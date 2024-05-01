import hashlib
import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from api.deps import SessionDep
from models.nvd import Nvd
from schemas.nvd import NvdCreate, NvdList

router = APIRouter()


@router.get("/", response_model=NvdList)
async def get_nvds(session: SessionDep, page: int = Query(1, ge=1), per_page: int = Query(10, le=100)) -> NvdList:
    count_statement = select(func.count()).select_from(Nvd)
    count = (await session.execute(count_statement)).one()[0]
    offset = (page - 1) * per_page
    statement = select(Nvd).offset(offset).limit(per_page)
    cves = (await session.execute(statement)).scalars().all()
    return NvdList(count=count, nvds=cves)


@router.get("/{id}")
async def read_nvd(session: SessionDep, id: str) -> Nvd:
    item = await session.get(Nvd, id)
    if not item:
        raise HTTPException(status_code=404, detail="Nvd not found")
    return item


@router.post("/")
async def create_nvd(session: SessionDep, nvd_in: NvdCreate) -> Nvd:
    nvd_in_hash_sum = hashlib.sha256(json.dumps(nvd_in.model_dump(), sort_keys=True).encode("utf-8")).hexdigest()
    print(nvd_in.model_dump())
    print(nvd_in_hash_sum)
    # existing_nvd = (await session.query(Nvd).filter(Nvd.hash_sum == nvd_in_hash_sum)).first()  # noqa: ERA001
    statement = select(Nvd).where(Nvd.hash_sum == nvd_in_hash_sum)
    result = await session.execute(statement)
    existing_nvd = result.one_or_none()
    if existing_nvd:
        raise HTTPException(status_code=409, detail="Duplicate data")

    nvd = Nvd.model_validate(nvd_in)
    nvd.hash_sum = nvd_in_hash_sum
    session.add(nvd)
    await session.commit()
    await session.refresh(nvd)
    return nvd


@router.put("/{id}")
async def update_nvd(session: SessionDep, id: str, nvd_in: NvdCreate) -> Nvd:
    item = await session.get(Nvd, id)
    if not item:
        raise HTTPException(status_code=404, detail="Nvd not found")
    nvd_in_hash_sum = hashlib.sha256(json.dumps(nvd_in.model_dump(), sort_keys=True).encode("utf-8")).hexdigest()
    # Update the fields of the existing Bdu object with the new data
    for key, value in nvd_in.model_dump().items():
        setattr(item, key, value)

    # Commit the changes and refresh the object
    item.updated_at = datetime.utcnow()  # noqa: DTZ003
    item.hash_sum = nvd_in_hash_sum
    await session.commit()
    await session.refresh(item)

    return item


@router.get("/cve_id/{cve_id}")
async def get_nvd_by_cve_id(session: SessionDep, cve_id: str) -> Nvd:
    statement = select(Nvd).where(Nvd.cve_id == cve_id)
    result = await session.execute(statement)
    nvd = result.scalar_one_or_none()
    if not nvd:
        raise HTTPException(status_code=404, detail="Cve not found")
    return nvd
