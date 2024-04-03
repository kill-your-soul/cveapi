from app.models.cwe import Cwe
from app.models.cve import Cve
from app.models.bdu import Bdu


metadata = [Bdu.metadata, Cwe.metadata, Cve.metadata]
