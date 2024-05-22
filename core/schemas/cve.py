from pydantic import BaseModel, ConfigDict, HttpUrl
from sqlalchemy_utils import URLType

from models.cve import Cve


class CveList(BaseModel):
    count: int
    cves: list[Cve]


class CveCreate(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    cve_id: str
    pocs: list[HttpUrl]
    references: list[HttpUrl]
