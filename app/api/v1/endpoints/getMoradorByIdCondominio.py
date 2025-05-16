
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_session
from app.schemas.morador import MoradorSchemaBase
router = APIRouter()

@router.get(
    "/{id_condominio}",
    summary="Recuperar todos os condominios",
    description="Busca todos os condominios com seus respectivos IDs e nomes.",
    response_description="Uma lista de condominios com seus IDs e nomes.",
    responses={
        200: {
            "description": "Resposta bem-sucedida com uma lista de condominios.",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {"id": 1, "nome": "Condominio 1"},
                        ]
                    }
                }
            },
        },
        500: {
            "description": "Erro interno do servidor.",
            "content": {
                "application/json": {
                    "example": {"detail": "Ocorreu um erro ao buscar os baralhos."}
                }
            },
        },
    },
)
async def get_all_decks(
    db: AsyncSession = Depends(get_session),
    id_condominio: int = 0
):
    try:
        moradores = await MoradorSchemaBase.get_all_moradores_by_id_condominio(session=db, id_condominio=id_condominio)
        return {"data": [{"id": morador.id, "nome": morador.nome} for morador in moradores]}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
