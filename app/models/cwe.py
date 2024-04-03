from app.models.base import BaseModel
from sqlmodel import Field, MetaData


class Cwe(BaseModel, table=True):
    metadata = MetaData()
    __tablename__ = "cwes"

    cwe_id: str = Field(index=True, nullable=False)
    name: str
    description: str
