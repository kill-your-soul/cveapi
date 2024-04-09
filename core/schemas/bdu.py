from pydantic import BaseModel


class BduCreate(BaseModel):
    bdu_id: str
    cve_id: str
    description: str
