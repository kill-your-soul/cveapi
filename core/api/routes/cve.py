from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from api.deps import SessionDep
from models.bdu import Bdu
from models.cve import Cve
from models.nvd import Nvd
from utils.color import get_color

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_cve(session: SessionDep, cve_id: str) -> dict[str, Any]:
    cve_id = cve_id.upper()
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


# TODO @kill_your_soul: remove this endpoint
@router.get("/html", response_class=HTMLResponse, deprecated=True)
async def get_html_cve(request: Request, session: SessionDep, cve_id: str):
    statement_bdu = select(Bdu).where(Bdu.cve_id == cve_id)
    statement_nvd = select(Nvd).where(Nvd.cve_id == cve_id)
    bdu_result = await session.execute(statement_bdu)
    nvd_result = await session.execute(statement_nvd)
    bdu_row = bdu_result.first()
    nvd_row = nvd_result.first()
    bdu: Bdu | None = bdu_row[0] if bdu_row else None
    nvd: Nvd | None = nvd_row[0] if nvd_row else None
    if not bdu and not nvd:
        raise HTTPException(status_code=404, detail="Info about given cve not found")
    # print(nvd)
    # if nvd.cvss3_score:
    #     score = {
    #         "base_score": nvd.cvss3,
    #         "vector":  json.loads(nvd.json)[""]
    #     }

    data = {
        "score": {
            "base_score": nvd.cvss3_score if nvd.cvss3_score else nvd.cvss2_score,
            "vector": nvd.cvss3_vector if nvd.cvss3_vector else nvd.cvss2_vector,
        },
        "description": bdu.description if bdu else nvd.summary,
        "ids": [obj_id for obj_id in [bdu.bdu_id if bdu else None, nvd.cve_id if nvd else None] if obj_id],
    }

    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={"id": cve_id, "data": data},
    )


# TODO @kill_your_soul: remove this endpoint
@router.get("/html2", response_class=HTMLResponse, deprecated=True)
async def get_html_cve(request: Request, session: SessionDep, cve_id: str):
    statement_bdu = select(Bdu).where(Bdu.cve_id == cve_id)
    statement_nvd = select(Nvd).where(Nvd.cve_id == cve_id)
    bdu_result = await session.execute(statement_bdu)
    nvd_result = await session.execute(statement_nvd)
    bdu_row = bdu_result.first()
    nvd_row = nvd_result.first()
    bdu: Bdu | None = bdu_row[0] if bdu_row else None
    nvd: Nvd | None = nvd_row[0] if nvd_row else None
    if not bdu and not nvd:
        raise HTTPException(status_code=404, detail="Info about given cve not found")
    # print(nvd)
    # if nvd.cvss3_score:
    #     score = {
    #         "base_score": nvd.cvss3,
    #         "vector":  json.loads(nvd.json)[""]
    #     }
    # print(nvd)
    # print(bdu)
    data = []
    if bdu:
        data.append(
            {
                "name": bdu.bdu_id,
                "description": bdu.description,
                "url": f"https://bdu.fstec.ru/vul/{bdu.bdu_id[4:]}",
            },
        )
    if nvd:
        data.append(
            {
                "name": nvd.cve_id,
                "description": nvd.summary,
                "score": {
                    "version": nvd.cvss3_vector.split("/")[0].split(":")[1] if nvd.cvss3_score else "2.0",
                    "base_score": nvd.cvss3_score if nvd.cvss3_score else nvd.cvss2_score,
                    "vector": nvd.cvss3_vector[9:] if nvd.cvss3_vector else nvd.cvss2_vector,
                },
                "url": f"https://nvd.nist.gov/vuln/detail/{nvd.cve_id}",
            },
        )

    return templates.TemplateResponse(
        request=request,
        name="base_2.html",
        context={"ids": data},
    )


@router.get("/many")
async def get_cves(request: Request, session: SessionDep, cve_ids: str):
    cves = [cve.strip().upper() for cve in cve_ids.split(",")]
    data = []
    for cve in cves:
        print(cve)
        statement_bdu = select(Bdu).where(Bdu.cve_id == cve)
        statement_nvd = select(Nvd).where(Nvd.cve_id == cve)
        statement_poc = select(Cve).where(Cve.cve_id == cve)
        poc_result = await session.execute(statement_poc)
        bdu_result = await session.execute(statement_bdu)
        nvd_result = await session.execute(statement_nvd)
        # bdu_row = bdu_result.first()
        # nvd_row = nvd_result.first()
        poc: Cve | None = poc_result.scalar_one_or_none()
        bdu: Bdu | None = bdu_result.scalar_one_or_none()
        nvd: Nvd | None = nvd_result.scalar_one_or_none()
        # bdu: Bdu | None = bdu_row[0] if bdu_row else None
        # nvd: Nvd | None = nvd_row[0] if nvd_row else None
        print(bdu)
        print(nvd)
        # poc: Cve | None = poc_row[0] if poc_row else None
        # print(poc)
        # print(poc.pocs)
        if not bdu and not nvd:
            continue
        tmp = {
            "ids": [],
        }
        if bdu:
            # data.append(
            #     {
            #         "name": bdu.bdu_id,
            #         "description": bdu.description,
            #         "url": f"https://bdu.fstec.ru/vul/{bdu.bdu_id[4:]}",
            #     },
            # )
            tmp["description"] = bdu.description
            tmp["ids"].append(
                {
                    "name": bdu.bdu_id,
                    "url": f"https://bdu.fstec.ru/vul/{bdu.bdu_id[4:]}",
                }
            )
        if nvd:
            # data.append(
            #     {
            #         "name": nvd.cve_id,
            #         "description": nvd.summary,
            #         "score": {
            #             "version": nvd.cvss3_vector.split("/")[0].split(":")[1] if nvd.cvss3_score else "2.0",
            #             "base_score": nvd.cvss3_score if nvd.cvss3_score else nvd.cvss2_score,
            #             "vector": nvd.cvss3_vector[9:] if nvd.cvss3_vector else nvd.cvss2_vector,
            #         },
            #         "url": f"https://nvd.nist.gov/vuln/detail/{nvd.cve_id}",
            #     },
            # )
            if "description" not in tmp:
                tmp["description"] = nvd.summary
            tmp["name"] = nvd.cve_id
            tmp["url"] = f"https://nvd.nist.gov/vuln/detail/{nvd.cve_id}"
            tmp["score"] = {
                "version": nvd.cvss3_vector.split("/")[0].split(":")[1] if nvd.cvss3_score else "2.0",
                "base_score": nvd.cvss3_score if nvd.cvss3_score else nvd.cvss2_score,
                "vector": nvd.cvss3_vector[9:] if nvd.cvss3_vector else nvd.cvss2_vector,
            }
            tmp["color"] = get_color(tmp["score"]["base_score"])
            # print(tmp["color"])
            tmp["ids"].append(
                {
                    "name": nvd.cve_id,
                    "url": f"https://nvd.nist.gov/vuln/detail/{nvd.cve_id}",
                }
            )
        if poc:
            tmp["pocs"] = poc.pocs
        # print(tmp["ids"])
        data.append(tmp)
        # tmp = {}
    # print(len(data))
    return templates.TemplateResponse(
        request=request,
        name="base_2.html",
        context={"data": data},
    )
