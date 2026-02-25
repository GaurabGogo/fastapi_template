from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.responses import send_response
from src.database.db import get_db
from src.users.repositories.user_repo import UserRepository
from src.users.schemas.user_schema import UserCreate, UserRead
from src.users.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["Users"])

async def get_user_service(
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)

# Type alias for cleaner dependency injection
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

@router.get("/")
async def list_users(
    service: UserServiceDep,
    page: int = 1,
    limit: int = 10,
    sort: str | None = None,
    name: str | None = None
):
    # Construct filters dict explicitly to use the parameters
    filters = {}
    if name:
        filters["name"] = name
    
    users, meta = await service.get_paginated_users(
        page=page,
        limit=limit,
        sort=sort,
        filters=filters
    )
    
    data = [UserRead.model_validate(u).model_dump() for u in users]
        
    return send_response(
        message="List of users", 
        data=data, 
        meta=meta
    )

@router.get("/{user_id}")
async def get_user(
    user_id: int, 
    service: UserServiceDep
):
    user = await service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    data = UserRead.model_validate(user).model_dump()
    return send_response(message="Get a User", data=data)

@router.post("/")
async def create_user(
    user_data: UserCreate, 
    service: UserServiceDep
):
    user = await service.create_user(user_data)
    data = UserRead.model_validate(user).model_dump()
    
    return send_response(
        message="Created a User", 
        data=data, 
        status_code=status.HTTP_201_CREATED
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    service: UserServiceDep
):
    success = await service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    return send_response(
        message="User deleted successfully", 
        status_code=status.HTTP_200_OK
    )
