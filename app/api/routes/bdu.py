from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.models.bdu import Bdu
from app.api.deps import SessionDep
from app.schemas.bdu import BduCreate

router = APIRouter()


@router.get("/")
async def get_bdus(session: SessionDep):
    statement = select(Bdu)
    cves = (await session.execute(statement)).scalars().all()
    return cves


@router.get("/{id}")
async def read_bdu(session: SessionDep, id: str):
    item = await session.get(Bdu, id)
    if not item:
        raise HTTPException(status_code=404, detail="Bdu not found")
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
