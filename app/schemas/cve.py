from pydantic import BaseModel


class CveCreate(BaseModel):
    cve_id: str
    json: dict
    vendors: dict
    cwes: dict
    summary: str
    cvss2: float
    cvss3: float
