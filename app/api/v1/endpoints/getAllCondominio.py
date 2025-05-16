
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_session
from app.schemas.condominio import CondominioSchemaBase
router = APIRouter()

@router.get(
    "/all",
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
async def get_all_condominios(
    db: AsyncSession = Depends(get_session)
):
    try:
        decks = await CondominioSchemaBase.get_all_decks(session=db)
        return {"data": [{"id": deck.id, "name": deck.nome} for deck in decks]}
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
