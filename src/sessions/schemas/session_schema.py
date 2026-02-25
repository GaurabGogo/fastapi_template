from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LocationBase(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    id: UUID
    session_id: UUID
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SessionBase(BaseModel):
    pass


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SessionBase):
    end_time: datetime | None = None


class SessionRead(SessionBase):
    id: UUID
    start_time: datetime
    end_time: datetime | None
    created_at: datetime
    updated_at: datetime
    locations: list[LocationRead] = []

    model_config = ConfigDict(from_attributes=True)
