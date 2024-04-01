import uuid
import sqlmodel as sa
from sqlmodel import Field
import datetime


class BaseModel(sa.SQLModel):
    __abstract__ = True

    id: uuid.UUID
    # created_at = db.Column(
    #     db.DateTime(timezone=True), default=db.func.now(), nullable=False, index=True
    # )
    created_at: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False))
    # updated_at = db.Column(
    #     db.DateTime(timezone=True),
    #     default=db.func.now(),
    #     onupdate=db.func.now(),
    #     nullable=False,
    # )
    updated_at: datetime.datetime = Field(sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False))
