from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.query_params import (
    apply_filters,
    apply_pagination,
    apply_sorting,
    get_pagination_meta,
)
from src.users.models.user import User
from src.users.schemas.user_schema import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_paginated(
        self, 
        page: int,
        limit: int,
        sort: str | None = None,
        filters: dict[str, Any] = None
    ) -> tuple[list[User], dict[str, Any]]:
        """
        Uses standard functional helpers to build the query.
        """
        filters = filters or {}
        
        # 1. Base Query
        stmt = select(User)
        
        # 2. Handle specialized partial search logic for name
        if "name" in filters and filters["name"]:
            search_val = filters.pop("name")
            stmt = stmt.where(User.name.ilike(f"%{search_val}%"))

        # 3. Apply other generic equality filters (age, etc.)
        stmt = apply_filters(stmt, User, filters)
        
        # 3. Get Total Count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total_count = total_result.scalar() or 0
        
        # 4. Apply Sorting & Pagination
        stmt = apply_sorting(stmt, User, sort)
        stmt = apply_pagination(stmt, page, limit)
        
        # 5. Execute
        result = await self.db.execute(stmt)
        users = result.scalars().all()
        
        # 6. Metadata
        meta = get_pagination_meta(total_count, page, limit)
        
        return list(users), meta

    async def get_all(self) -> list[User]:
        stmt = select(User)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create(self, user_data: UserCreate) -> User:
        user = User(name=user_data.name, age=user_data.age)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if not user:
            return False
        
        await self.db.delete(user)
        await self.db.commit()
        return True
