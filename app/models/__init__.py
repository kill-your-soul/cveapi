from app.models.cwe import Cwe
from app.models.nvd import Nvd
from app.models.bdu import Bdu


metadata = [Bdu.metadata, Cwe.metadata, Nvd.metadata]
