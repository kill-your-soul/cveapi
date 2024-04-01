import sqlmodel
from . import BaseModel


class Bdu(BaseModel):
    __tablename__ = "bdus"

    bdu_id = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

