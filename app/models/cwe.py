from . import BaseModel
from sqlmodel import Field


class Cwe(BaseModel, table=True):
    __tablename__ = "cwes"

    cwe_id: str = Field(index=True, nullable=False)
    name: str
    description: str
