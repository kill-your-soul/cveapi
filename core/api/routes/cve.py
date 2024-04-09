from typing import Any

from fastapi import APIRouter
from sqlmodel import select

from core.api.deps import SessionDep
from core.models.bdu import Bdu
from core.models.nvd import Nvd

router = APIRouter()


@router.get("/")
async def get_cve(session: SessionDep, cve_id: str) -> dict[str, Any]:
    statement_bdu = select(Bdu).where(Bdu.cve_id == cve_id)
    statement_nvd = select(Nvd).where(Nvd.cve_id == cve_id)
    bdu_result = await session.execute(statement_bdu)
    nvd_result = await session.execute(statement_nvd)
    bdu_row = bdu_result.first()
    nvd_row = nvd_result.first()
    bdu = bdu_row[0] if bdu_row else None
    nvd = nvd_row[0] if nvd_row else None

    response = {}
    if bdu:
        response["bdu"] = bdu.model_dump(exclude={"created_at", "updated_at"})
    else:
        response["bdu"] = None
    if nvd:
        response["nvd"] = nvd.model_dump(exclude={"created_at", "updated_at"})
    else:
        response["nvd"] = None

    return response
