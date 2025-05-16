from fastapi import APIRouter, Depends
from app.api.v1.endpoints import (
    test,
    getAllCondominio,
    getMoradorByIdCondominio,
    postNewColeta,   
    getAllColeta,
    getChat
)

api_router = APIRouter()
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(
    getAllCondominio.router, prefix="/condominio", tags=["condominio"]
)
api_router.include_router(
    getMoradorByIdCondominio.router, prefix="/morador", tags=["morador"]
)
api_router.include_router(
    postNewColeta.router, prefix="/coleta", tags=["coleta"]
)       

api_router.include_router(
    getAllColeta.router, prefix="/coleta", tags=["coleta"]
)
api_router.include_router(
    getChat.router, prefix="/chat", tags=["chat"]
)
