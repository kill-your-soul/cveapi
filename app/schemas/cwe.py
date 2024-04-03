from pydantic import BaseModel


class CweCreate(BaseModel):
    cwe_id: str
    name: str
    description: str
