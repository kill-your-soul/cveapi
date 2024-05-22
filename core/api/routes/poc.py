import hashlib
import json
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from api.deps import SessionDep
from models.cve import Cve
from schemas.cve import CveCreate, CveList

router = APIRouter()


@router.get("/{id}", response_model=Cve)
async def read_cve_by_id(session: SessionDep, id: str) -> Cve:
    item = await session.get(Cve, id)
    if not item:
        raise HTTPException(status_code=404, detail="Bdu not found")
    return item

@router.get("/", response_model=CveList)
async def get_pocs(session: SessionDep, page: int = Query(1, ge=1), per_page: int = Query(10, le=100))-> CveList:
    count_statement = select(func.count()).select_from(Cve)
    count = (await session.execute(count_statement)).one()[0]
    offset = (page - 1) * per_page
    statement = select(Cve).offset(offset).limit(per_page)
    pocs = (await session.execute(statement)).scalars().all()
    return CveList(count=count, cves=pocs)

@router.get("/cve_id/{cve_id}")
async def get_nvd_by_cve_id(session: SessionDep, cve_id: str) -> Cve:
    statement = select(Cve).where(Cve.cve_id == cve_id)
    result = await session.execute(statement)
    cve = result.scalar_one_or_none()
    if not cve:
        raise HTTPException(status_code=404, detail="Cve not found")
    return cve


@router.put("/{id}")
async def update_poc(session: SessionDep, id: str, nvd_in: CveCreate) -> Cve:
    item = await session.get(Cve, id)
    if not item:
        raise HTTPException(status_code=404, detail="Cve not found")
    cve_in_hash_sum = hashlib.sha256(json.dumps(nvd_in.model_dump(), sort_keys=True).encode("utf-8")).hexdigest()
    # Update the fields of the existing Bdu object with the new data
    for key, value in nvd_in.model_dump().items():
        setattr(item, key, value)

    # Commit the changes and refresh the object
    item.updated_at = datetime.utcnow()  # noqa: DTZ003
    item.hash_sum = cve_in_hash_sum
    await session.commit()
    await session.refresh(item)

    return item


@router.post("/")
async def create_poc(session: SessionDep, nvd_in: CveCreate) -> Cve:
    # Преобразуем объекты HttpUrl в строки
    nvd_in_dict = nvd_in.dict()
    nvd_in_dict["pocs"] = [str(url) for url in nvd_in_dict["pocs"]]
    nvd_in_dict["references"] = [str(url) for url in nvd_in_dict["references"]]
    nvd_in_hash_sum = hashlib.sha256(json.dumps(nvd_in_dict, sort_keys=True).encode("utf-8")).hexdigest()
    print(nvd_in_dict)
    print(nvd_in_hash_sum)
    statement = select(Cve).where(Cve.hash_sum == nvd_in_hash_sum)
    result = await session.execute(statement)
    existing_nvd = result.scalars().first()
    if existing_nvd:
        raise HTTPException(status_code=409, detail="Duplicate data")

    cve = Cve(**nvd_in_dict)
    cve.hash_sum = nvd_in_hash_sum
    session.add(cve)
    await session.commit()
    await session.refresh(cve)
    return cve
