from pydantic import BaseModel

from models.cwe import Cwe


class CweCreate(BaseModel):
    cwe_id: str
    name: str
    description: str


class CweList(BaseModel):
    count: int
    cwes: list[Cwe]
