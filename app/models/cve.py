from sqlmodel import Field, SQLModel, Uuid
from . import BaseModel


# class CveBase(BaseModel):
#     cve_id = db.Column(db.String(), nullable=False)
#     json = db.Column(JSONB)
#
#     # We used initially secondary relationships to fetch the list of
#     # associated vendors, products and cwes. But it was complicated
#     # to maintain, and the performance were poor. So we now use the
#     # JSONB data type associated to the GIN index type.
#     vendors = db.Column(JSONB)
#     cwes = db.Column(JSONB)
#
#     # Keep the summary separated when searching keywords
#     summary = db.Column(db.String(), nullable=False)
#
#     # Keep CVSS separated when searching a particupal score
#     cvss2 = db.Column(db.Float())
#     cvss3 = db.Column(db.Float())

