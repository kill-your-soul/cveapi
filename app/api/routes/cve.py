from fastapi import APIRouter
from sqlmodel import select

from app.api.deps import SessionDep
from app.models.bdu import Bdu
from app.models.nvd import Nvd


router = APIRouter()

@router.get("/")
async def get_cve(session: SessionDep, cve_id: str):
    statement_bdu = select(Bdu).where(Bdu.cve_id == cve_id)
    statement_nvd = select(Nvd).where(Nvd.cve_id == cve_id)
    bdu = (await session.execute(statement_bdu)).first()[0]
    nvd = (await session.execute(statement_nvd)).first()[0]
    return {"bdu": bdu.model_dump(exclude={"created_at", "updated_at"}), "nvd": nvd.model_dump(exclude={"created_at", "updated_at"})}
