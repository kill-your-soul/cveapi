from sqlmodel import Field, MetaData

from models.base import BaseModel


class Cwe(BaseModel, table=True):
    metadata = MetaData()
    __tablename__ = "cwes"

    cwe_id: str = Field(index=True, nullable=False)
    name: str
    description: str
