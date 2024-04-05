from sqlmodel import Field, MetaData

from app.models.base import BaseModel


class Bdu(BaseModel, table=True):
    metadata = MetaData()
    __tablename__ = "bdus"

    bdu_id: str = Field(nullable=False)
    cve_id: str = Field(nullable=False)
    description: str = Field(nullable=False)
