from typing import Any

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

    async def create_user(self, user_data: UserCreate) -> User:
        return await self.repository.create(user_data)

    async def delete_user(self, user_id: int) -> bool:
        return await self.repository.delete(user_id)
