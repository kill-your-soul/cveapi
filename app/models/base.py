from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()), nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    hash_sum: str = Field(default=None, unique=True, index=True, nullable=False)

    def to_dict(self, attrs) -> dict[Any, str]:  # noqa: ANN001
        return {attr: str(getattr(self, attr)) for attr in attrs}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} '{self.id}'>"
