from fastapi import APIRouter
from sqlmodel import select, func
from app.models.cwe import Cwe
from app.api.deps import SessionDep
from app.schemas.cwe import CweCreate

router = APIRouter()


@router.get("/")
async def get_cwes(session: SessionDep):
    count_statement = (
        select(func.count())
        .select_from(Cwe)
    )
    count = (await session.execute(count_statement)).one()
    statement = select(Cwe)
    cves = (await session.execute(statement)).scalars().all()
    return cves


@router.get("/{id}")
async def read_cwe(session: SessionDep, id: str):
    item = await session.get(Cwe, id)
    return item


@router.post("/")
async def create_cwe(session: SessionDep, bdu_in: CweCreate):
    cve = Cwe.model_validate(bdu_in)
    session.add(cve)
    await session.commit()
    await session.refresh(cve)
    return cve
