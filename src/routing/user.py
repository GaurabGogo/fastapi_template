from fastapi import APIRouter, Depends
from src.models.user import CreateUser
from typing import Annotated
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.database.schema.user_schema import UserSchema
from sqlalchemy import select

router = APIRouter(prefix="/user", dependencies=[])



@router.get("/")
def index(
    db: Annotated[Session, Depends(get_db)],
):
    stmt = select(UserSchema.id, UserSchema.name, UserSchema.age)

    users = db.execute(stmt).mappings().all()
    return {
        "message": "List of users",
        "data": users,
    }


@router.get("/{id}")
def show(id: int, db: Annotated[Session, Depends(get_db)]):

    user = db.query(UserSchema).filter(UserSchema.id == id).first()
    return {"message": "Get a User", "data": user}


@router.post("/")
def store(item: CreateUser, db: Annotated[Session, Depends(get_db)]):
    user = UserSchema(name=item.name, age=item.age)
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Created a User", "data": user}




@router.delete("/{id}")
def delete(id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.query(UserSchema).filter(UserSchema.id == id).first()
    if not user:
        return {"message": "User not found"}

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
