from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from api.deps import SessionDep
from models.bdu import Bdu
from models.nvd import Nvd

router = APIRouter()
templates = Jinja2Templates(directory="templates")


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


@router.get("/html", response_class=HTMLResponse)
async def get_html_cve(request: Request, session: SessionDep, cve_id: str):
    statement_bdu = select(Bdu).where(Bdu.cve_id == cve_id)
    statement_nvd = select(Nvd).where(Nvd.cve_id == cve_id)
    bdu_result = await session.execute(statement_bdu)
    nvd_result = await session.execute(statement_nvd)
    bdu_row = bdu_result.first()
    nvd_row = nvd_result.first()
    bdu: Bdu | None = bdu_row[0] if bdu_row else None
    nvd: Nvd | None = nvd_row[0] if nvd_row else None
    # print(bdu.description)
    data = {
        "score": {"base_score": 1, "vector": 2},
        "description": bdu.description if bdu else "",
        "ids": [bdu.bdu_id, nvd.cve_id],
    }

    # TODO @kill_your_soul: Edit template to include all data
    return templates.TemplateResponse(
        request=request, name="base.html", context={"id": cve_id, "data": data},
    )
