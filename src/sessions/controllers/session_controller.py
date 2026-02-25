from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.responses import send_response
from src.database.db import get_db
from src.sessions.schemas.session_schema import (
    LocationCreate,
    LocationRead,
    SessionRead,
)
from src.sessions.services.session_service import SessionService
from src.core.security import is_authenticated
from src.users.models.user import User

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/start", status_code=status.HTTP_201_CREATED)
async def start_session(
    current_user: Annotated[User, Depends(is_authenticated)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = SessionService(db)
    session = await service.start_session(current_user.id)
    return send_response(
        message="Session started successfully",
        data=SessionRead.model_validate(session),
        status_code=status.HTTP_201_CREATED
    )


@router.post("/{session_id}/location", status_code=status.HTTP_201_CREATED)
async def add_location(
    session_id: UUID,
    location_data: LocationCreate,
    current_user: Annotated[User, Depends(is_authenticated)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = SessionService(db)
    location = await service.add_location(session_id, location_data)
    return send_response(
        message="Location recorded successfully",
        data=LocationRead.model_validate(location),
        status_code=status.HTTP_201_CREATED
    )


@router.post("/{session_id}/end")
async def end_session(
    session_id: UUID,
    current_user: Annotated[User, Depends(is_authenticated)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = SessionService(db)
    session = await service.end_session(session_id)
    return send_response(
        message="Session ended successfully",
        data=SessionRead.model_validate(session)
    )


@router.get("/{session_id}")
async def get_session(
    session_id: UUID,
    current_user: Annotated[User, Depends(is_authenticated)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = SessionService(db)
    session = await service.get_session_details(session_id)
    return send_response(
        message="Session details retrieved successfully",
        data=SessionRead.model_validate(session)
    )
