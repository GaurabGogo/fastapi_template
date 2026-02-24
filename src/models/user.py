from pydantic import BaseModel, Field
from typing import Optional


class CreateUser(BaseModel):
    name: str = Field(..., max_length=50, min_length=5)
    age: Optional[int] = Field(None, ge=18, le=99)