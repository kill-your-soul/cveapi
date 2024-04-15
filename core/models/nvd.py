from sqlalchemy import JSON
from sqlmodel import Column, Field, MetaData

from models.base import BaseModel


class Nvd(BaseModel, table=True):
    metadata = MetaData()
    __tablename__ = "nvds"

    cve_id: str = Field(nullable=False)
    json: dict = Field(sa_column=Column(JSON), default={})

    # We used initially secondary relationships to fetch the list of
    # associated vendors, products and cwes. But it was complicated
    # to maintain, and the performance were poor. So we now use the
    # JSONB data type associated to the GIN index type.
    vendors: dict = Field(sa_column=Column(JSON), default={})
    cwes: dict = Field(sa_column=Column(JSON), default={})

    # Keep the summary separated when searching keywords
    summary: str = Field(nullable=False)

    # Keep CVSS separated when searching a particular score
    cvss2: float = Field(nullable=True)
    cvss3: float = Field(nullable=True)
