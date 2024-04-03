from fastapi import APIRouter
from sqlmodel import select, func
from app.models.cve import Cve
from app.api.deps import SessionDep
from app.schemas.cve import CveCreate

router = APIRouter()


@router.get("/")
async def get_cves(session: SessionDep):
    count_statement = (
        select(func.count())
        .select_from(Cve)
    )
    count = (await session.execute(count_statement)).one()
    statement = select(Cve)
    cves = (await session.execute(statement)).scalars().all()
    return cves


@router.get("/{id}")
async def read_cve(session: SessionDep, id: str):
    item = await session.get(Cve, id)
    return item


@router.post("/")
async def create_cve(session: SessionDep, bdu_in: CveCreate):
    cve = Cve.model_validate(bdu_in)
    session.add(cve)
    await session.commit()
    await session.refresh(cve)
    return cve
