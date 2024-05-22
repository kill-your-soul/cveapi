from pydantic import ConfigDict
from sqlalchemy_utils import URLType
from sqlmodel import ARRAY, Column, Field, MetaData

from models.base import BaseModel


class Cve(BaseModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metadata = MetaData()
    __tablename__ = "cves"

    cve_id: str
    # poc: ARRAY[str]
    # references: ARRAY[str]
    pocs: list[str] = Field(sa_column=Column(ARRAY(URLType), nullable=True))
    references: list[str] = Field(sa_column=Column(ARRAY(URLType), nullable=True))

