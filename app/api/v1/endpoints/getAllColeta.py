from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_session
from app.schemas.morador import MoradorSchemaBase
from app.schemas.coleta import ColetaSchemaBase
from app.services.computevision import classificar_imagem_azure
from datetime import datetime
router = APIRouter()

@router.get(
    "/{id_condominio}/{id_morador}",
    summary="Retorna todas as coletas de um morador",
    description="Retorna todas as coletas de um morador específico.",
    response_description="Retorna uma lista com todas as coletas do morador.",
    responses={
        200: {
            "description": "Resposta bem-sucedida com uma lista de coletas.",
            "content": {
                "application/json": {
                    "example": {
                        "coletas": [
                            {
                                "id": 2,
                                "residuos": ["lata", "lata", "pet"],
                                "data": "2025-05-16T08:47:12.401987",
                                "morador": 1,
                                "condominio": 1
                            },
                            {
                                "id": 3,
                                "residuos": ["lata", "lata", "pet"],
                                "data": "2025-05-16T09:11:42.674995",
                                "morador": 1,
                                "condominio": 1
                            }
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Nenhuma coleta encontrada para o morador.",
            "content": {
                "application/json": {
                    "example": {"detail": "Nenhuma coleta encontrada para o morador."}
                }
            },
        },
        500: {
            "description": "Erro interno do servidor.",
            "content": {
                "application/json": {
                    "example": {"detail": "Ocorreu um erro ao buscar os moradores."}
                }
            },
        },
    },
)
async def post_new_coleta(
    id_condominio: int,
    id_morador: int,
    db: AsyncSession = Depends(get_session),
):
    try:
        # pega todos as coletas do morador
        coletas = await ColetaSchemaBase.retornar_coletas(db, morador=id_morador, condominio=id_condominio)
        if not coletas:
            raise HTTPException(status_code=404, detail="Nenhuma coleta encontrada para o morador.")
        
        # Formata a resposta
        resposta = [
            {
                "id": coleta.id,
                "residuos": coleta.residuos,
                "data": coleta.data,
                "morador": coleta.morador,
                "condominio": coleta.condominio
            }
            for coleta in coletas
        ]   
        # Retorna a resposta
        return {
            "coletas": resposta
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
