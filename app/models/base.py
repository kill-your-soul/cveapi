from sqlmodel import SQLModel, Field
from uuid import uuid4
from datetime import datetime


class BaseModel(SQLModel):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid4()), nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    def to_dict(self, attrs):
        return {attr: str(getattr(self, attr)) for attr in attrs}

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.id}'>"