import datetime
import hashlib
import json

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from api.deps import SessionDep
from models.cwe import Cwe
from schemas.cwe import CweCreate, CweList

router = APIRouter()


@router.get("/", response_model=CweList)
async def get_cwes(session: SessionDep, page: int = Query(1, ge=1), per_page: int = Query(10, le=100)) -> CweList:
    count_statement = select(func.count()).select_from(Cwe)
    count = (await session.execute(count_statement)).one()[0]
    offset = (page - 1) * per_page
    statement = select(Cwe).offset(offset).limit(per_page)
    cwes = (await session.execute(statement)).scalars().all()
    return CweList(count=count, cwes=cwes)


@router.get("/{id}")
async def read_cwe(session: SessionDep, id: str) -> Cwe:
    item = await session.get(Cwe, id)
    if not item:
        raise HTTPException(status_code=404, detail="Cwe not found")
    return item


@router.post("/")
async def create_cwe(session: SessionDep, cwe_in: CweCreate) -> Cwe:
    cwe_in_hash_sum = hashlib.sha256(json.dumps(cwe_in.model_dump(), sort_keys=True).encode("utf-8")).hexdigest()
    statement = select(Cwe).where(Cwe.hash_sum == cwe_in_hash_sum)
    result = await session.execute(statement)
    existing_nvd = result.one_or_none()
    if existing_nvd:
        raise HTTPException(status_code=409, detail="Duplicate data")

    cwe: Cwe = Cwe.model_validate(cwe_in)
    cwe.hash_sum = cwe_in_hash_sum
    session.add(cwe)
    await session.commit()
    await session.refresh(cwe)
    return cwe


@router.get("/cwe_id/{cwe_id}")
async def get_cwe_by_id(session: SessionDep, cwe_id: str):
    statement = select(Cwe).where(Cwe.cwe_id == cwe_id)
    result = await session.execute(statement)
    nvd = result.scalar_one_or_none()
    if not nvd:
        raise HTTPException(status_code=404, detail="Cwe not found")
    return nvd


@router.put("/{id}")
async def update_cwe(session: SessionDep, id: str, cwe_in: CweCreate) -> Cwe:
    item = await session.get(Cwe, id)
    if not item:
        raise HTTPException(status_code=404, detail="Cwe not found")

    # Update the fields of the existing Bdu object with the new data
    for key, value in cwe_in.model_dump().items():
        setattr(item, key, value)

    # Commit the changes and refresh the object
    item.updated_at = datetime.utcnow() # type: ignore  # noqa: PGH003
    await session.commit()
    await session.refresh(item)

    return item
