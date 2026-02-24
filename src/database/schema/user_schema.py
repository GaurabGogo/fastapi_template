from sqlalchemy import Integer, String, Boolean, DateTime, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from ..db import Base
from datetime import datetime, timezone


class UserSchema(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(VARCHAR(100), nullable=False, index=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.now(timezone.utc)
    )
