from typing import Any

from pydantic import BaseModel


class Nvd(BaseModel):
    cve_id: str
    json: dict[Any, Any]
    vendors: dict[str, Any]
    cwes: dict[str, Any]
    summary: str
    cvss2: float
    cvss3: float


class Bdu(BaseModel):
    bdu_id: str
    cve_id: str
    description: str


class Cwe(BaseModel):
    cwe_id: str
    name: str
    description: str


class Cve(BaseModel):
    cve_id: str
    pocs: list[str]
    references: list[str]
