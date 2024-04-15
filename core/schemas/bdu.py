from pydantic import BaseModel

from models.bdu import Bdu


class BduCreate(BaseModel):
    bdu_id: str
    cve_id: str
    description: str


class ListBdu(BaseModel):
    count: int
    bdus: list[Bdu]
