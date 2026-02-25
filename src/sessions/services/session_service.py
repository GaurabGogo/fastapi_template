from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.sessions.repositories.session_repo import SessionRepository
from src.sessions.schemas.session_schema import LocationCreate


class SessionService:
    def __init__(self, db: AsyncSession):
        self.repo = SessionRepository(db)

    async def start_session(self):
        session = await self.repo.create_session()
        return await self.repo.get_session(session.id)

    async def add_location(self, session_id: UUID, location_data: LocationCreate):
        session = await self.repo.get_session(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
            
        if session.end_time is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot add location to an already ended session"
            )
            
        return await self.repo.add_location(
            session_id=session_id,
            latitude=location_data.latitude,
            longitude=location_data.longitude
        )

    async def end_session(self, session_id: UUID):
        session = await self.repo.get_session(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
            
        if session.end_time is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session is already ended"
            )
            
        await self.repo.end_session(session)
        return await self.repo.get_session(session_id)

    async def get_session_details(self, session_id: UUID):
        session = await self.repo.get_session(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
            
        return session
