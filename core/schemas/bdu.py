from pydantic import BaseModel

from models.bdu import Bdu


class BduCreate(BaseModel):
    bdu_id: str
    cve_id: str
    description: str


class BduList(BaseModel):
    count: int
    bdus: list[Bdu]


class BduOut(BaseModel):
    id: str
    bdu_id: str
    cves: list[str]
    description: str
    hash_sum: str
