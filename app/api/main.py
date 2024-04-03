from fastapi import APIRouter
from app.api.routes import cve, bdu, cwe

# TODO: Add import routes

api_router = APIRouter()
api_router.include_router(cve.router, prefix="/cve", tags=["cve"])
api_router.include_router(bdu.router, prefix="/bdu", tags=["bdu"])
api_router.include_router(cwe.router, prefix="/cwe", tags=["cwe"])
