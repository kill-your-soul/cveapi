from typing import Any, Dict
from pydantic import BaseModel


class NvdCreate(BaseModel):
    cve_id: str
    json: dict
    vendors: Dict[str, Any]
    cwes: Dict[str, Any]
    summary: str
    cvss2: float
    cvss3: float
