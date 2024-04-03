from fastapi import APIRouter, Query
from sqlmodel import select
from app.models.nvd import Nvd
from app.api.deps import SessionDep
from app.schemas.nvd import NvdCreate

router = APIRouter()


@router.get("/")
async def get_nvds(session: SessionDep, page: int = Query(1, ge=1), per_page: int = Query(10, le=100)):
    offset = (page - 1) * per_page
    
    # Создаем запрос SQLAlchemy
    statement = select(Nvd).offset(offset).limit(per_page)
    cves = (await session.execute(statement)).scalars().all()
    return cves


@router.get("/{id}")
async def read_nvd(session: SessionDep, id: str):
    item = await session.get(Nvd, id)
    return item


@router.post("/")
async def create_nvd(session: SessionDep, bdu_in: NvdCreate):
    cve = Nvd.model_validate(bdu_in)
    session.add(cve)
    await session.commit()
    await session.refresh(cve)
    return cve
