import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from api.deps import SessionDep
from models.cwe import Cwe
from schemas.cwe import CweCreate

router = APIRouter()


@router.get("/")
async def get_cwes(session: SessionDep) -> list[Cwe]:
    statement = select(Cwe)
    cves = (await session.execute(statement)).scalars().all()
    return cves


@router.get("/{id}")
async def read_cwe(session: SessionDep, id: str) -> Cwe:
    item = await session.get(Cwe, id)
    if not item:
        raise HTTPException(status_code=404, detail="Cwe not found")
    return item


@router.post("/")
async def create_cwe(session: SessionDep, cwe_in: CweCreate) -> Cwe:
    cve = Cwe.model_validate(cwe_in)
    session.add(cve)
    await session.commit()
    await session.refresh(cve)
    return cve


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
