from fastapi import APIRouter

from core.api.routes import bdu, cve, cwe, nvd

api_router = APIRouter()
api_router.include_router(nvd.router, prefix="/nvd", tags=["nvd"])
api_router.include_router(bdu.router, prefix="/bdu", tags=["bdu"])
api_router.include_router(cwe.router, prefix="/cwe", tags=["cwe"])
api_router.include_router(cve.router, prefix="/cve", tags=["cve"])
