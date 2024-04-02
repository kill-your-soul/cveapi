from . import BaseModel
from sqlmodel import Field, MetaData


class Bdu(BaseModel, table=True):
    metadata = MetaData()
    __tablename__ = "bdus"

    bdu_id: str = Field(primary_key=True)
    description: str = Field(nullable=False)
