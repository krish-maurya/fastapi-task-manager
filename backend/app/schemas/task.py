from datetime import datetime
from html import escape

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

    # Basic sanitization blocks direct script/html injection in stored text.
    @field_validator("title", "description")
    @classmethod
    def sanitize_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return escape(value.strip())


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

    @field_validator("title", "description")
    @classmethod
    def sanitize_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return escape(value.strip())


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
