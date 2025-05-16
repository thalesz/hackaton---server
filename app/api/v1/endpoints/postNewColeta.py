from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_session
from app.schemas.morador import MoradorSchemaBase
from app.schemas.coleta import ColetaSchemaBase
from app.services.computevision import classificar_imagem_azure
from datetime import datetime
router = APIRouter()

@router.post(
    "/{id_condominio}/{id_morador}",
    summary="Realizar coleta de resíduos",
    description="Realiza a coleta de resíduos de um morador específico.",
    response_description="Informa se a coleta foi realizada com sucesso e a resposta da visão computacional.",
    responses={
        200: {
            "description": "Resposta bem-sucedida com uma lista de moradores.",
            "content": {
                "application/json": {
                    "example": {
                        "data": [
                            {"mensagem": "Coleta realizada com sucesso", "resposta": "Papel, vidro"},
                        ]
                    }
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
    img: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
):
    try:
        if img.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Formato de imagem não suportado. Envie JPEG ou PNG.")

        conteudo = await img.read()
        resultado_classificacao = await classificar_imagem_azure(conteudo)

        # Filtrar apenas os itens com probabilidade > 0.6
        predicoes_filtradas = [
            pred["tagName"]
            for pred in resultado_classificacao.get("predictions", [])
            if pred["probability"] > 0.5
        ]

        # Contar a quantidade de cada item
        from collections import Counter
        contagem = Counter(predicoes_filtradas)

        # Transformar em lista de dicionários com nome e quantidade
        resposta_final = [{"nome": nome, "quantidade": quantidade} for nome, quantidade in contagem.items()]

        #salvar a coleta no banco de dados
        coleta = await ColetaSchemaBase.criar_coleta(
            session=db,
            residuos=predicoes_filtradas,
            data=datetime.now(), 
            morador=id_morador,
            condominio=id_condominio
        )
        
        return {
            "mensagem": "Coleta realizada com sucesso",
            "resposta": resposta_final,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
