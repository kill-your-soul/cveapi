from typing import Any

from pydantic import BaseModel


class NvdCreate(BaseModel):
    cve_id: str
    json: dict[Any, Any]
    vendors: dict[str, Any]
    cwes: dict[str, Any]
    summary: str
    cvss2: float
    cvss3: float
