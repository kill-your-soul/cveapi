import hashlib
import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from api.deps import SessionDep
from models.bdu import Bdu
from schemas.bdu import BduCreate, ListBdu

router = APIRouter()


@router.get("/", response_model=ListBdu)
async def get_bdus(session: SessionDep, page: int = Query(1, ge=1), per_page: int = Query(10, le=100)) -> ListBdu:
    count_statement = select(func.count()).select_from(Bdu)
    count = (await session.execute(count_statement)).one()[0]
    offset = (page - 1) * per_page
    statement = select(Bdu).offset(offset).limit(per_page)
    bdus = (await session.execute(statement)).scalars().all()
    return ListBdu(count=count, bdus=bdus)


@router.get("/{id}")
async def read_bdu(session: SessionDep, id: str) -> Bdu:
    item = await session.get(Bdu, id)
    if not item:
        raise HTTPException(status_code=404, detail="Bdu not found")
    return item


@router.post("/", response_model=Bdu)
async def create_bdu(session: SessionDep, bdu_in: BduCreate) -> Bdu:
    bdu_in_hash_sum = hashlib.sha256(json.dumps(bdu_in.model_dump(), sort_keys=True).encode()).hexdigest()
    statement = select(Bdu).where(Bdu.hash_sum == bdu_in_hash_sum)
    result = await session.execute(statement)
    existing_bdu = result.one_or_none()
    if existing_bdu:
        raise HTTPException(status_code=409, detail="Duplicate data")
    bdu = Bdu.model_validate(bdu_in)
    bdu.hash_sum = bdu_in_hash_sum
    session.add(bdu)
    await session.commit()
    await session.refresh(bdu)
    return bdu


@router.put("/{id}")
async def update_bdu(session: SessionDep, id: str, bdu_in: BduCreate) -> Bdu:
    item = await session.get(Bdu, id)
    if not item:
        raise HTTPException(status_code=404, detail="Bdu not found")

    # Update the fields of the existing Bdu object with the new data
    for key, value in bdu_in.model_dump().items():
        setattr(item, key, value)

    # Commit the changes and refresh the object
    item.updated_at = datetime.utcnow()  # noqa: DTZ003
    await session.commit()
    await session.refresh(item)

    return item
