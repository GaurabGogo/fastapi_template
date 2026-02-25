from typing import Any

from src.core.security import get_password_hash, verify_password
from src.users.models.user import User
from src.users.repositories.user_repo import UserRepository
from src.users.schemas.user_schema import UserCreate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_paginated_users(
        self, 
        page: int,
        limit: int,
        sort: str | None = None,
        filters: dict[str, Any] = None
    ) -> tuple[list[User], dict[str, Any]]:
        return await self.repository.get_all_paginated(
            page=page, 
            limit=limit, 
            sort=sort, 
            filters=filters
        )

    async def get_all_users(self) -> list[User]:
        return await self.repository.get_all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_by_email(email)

    async def create_user(self, user_data: UserCreate) -> User:
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
            
        hashed_password = get_password_hash(user_data.password)
        return await self.repository.create(user_data, hashed_password)

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)
