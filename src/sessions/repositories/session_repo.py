from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.sessions.models.session import Location, Session


class SessionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self) -> Session:
        session = Session()
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session(self, session_id: UUID) -> Session | None:
        stmt = (
            select(Session)
            .where(Session.id == session_id)
            .options(selectinload(Session.locations))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def add_location(
        self, 
        session_id: UUID, 
        latitude: float, 
        longitude: float
    ) -> Location:
        location = Location(
            session_id=session_id,
            latitude=latitude,
            longitude=longitude
        )
        self.db.add(location)
        await self.db.commit()
        await self.db.refresh(location)
        return location

    async def end_session(self, session: Session) -> Session:
        session.end_time = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(session)
        return session
