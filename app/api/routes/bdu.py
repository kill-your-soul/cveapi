from fastapi import APIRouter
from sqlmodel import select, func
from app.models.bdu import Bdu
from app.api.deps import SessionDep
from app.schemas.bdu import BduCreate

router = APIRouter()


@router.get("/")
async def get_bdus(session: SessionDep):
    count_statement = (
        select(func.count())
        .select_from(Bdu)
    )
    count = (await session.execute(count_statement)).one()
    statement = select(Bdu)
    cves = (await session.execute(statement)).scalars().all()
    return cves


@router.get("/{id}")
async def read_bdu(session: SessionDep, id: str):
    item = await session.get(Bdu, id)
    return item


@router.post("/")
async def create_bdu(session: SessionDep, bdu_in: BduCreate):
    print(session)
    bdu = Bdu.model_validate(bdu_in)
    print(bdu)
    session.add(bdu)
    await session.commit()
    await session.refresh(bdu)
    return bdu
