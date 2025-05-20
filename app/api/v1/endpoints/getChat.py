from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_session
from app.services.computevision import classificar_imagem_azure
from app.services.openai import gerar_texto
from datetime import datetime
from collections import Counter
import re
import json

router = APIRouter()

async def gerar_orientacoes_reciclagem(materiais: list[str], prompt: str) -> tuple[str, str]:
    if materiais:
        materiais_texto = ", ".join(materiais)
        prompt_final = (
            f"{prompt}\n\n"
            f"Foram detectados os seguintes materiais na imagem: {materiais_texto}.\n\n"
            f"Com base nesses materiais, escreva um texto claro, direto e fácil de entender, explicando como a pessoa deve armazenar corretamente cada um deles até que o serviço de coleta passe para retirar. "
            f"Não mencione locais de descarte nem centros de reciclagem — só diga como guardar de forma segura, higiênica e responsável dentro de casa.\n\n"
            f"Importante: responda apenas com o texto da orientação. Não use formatação extra, listas, JSON ou estrutura de dicionário. Não adicione explicações fora da mensagem. Apenas o texto direto com as instruções.\n"
            f"Exemplo de resposta: 'Garrafas PET devem ser lavadas, secas e armazenadas em sacos plásticos transparentes. Caixas de papelão podem ser desmontadas e mantidas em local seco até a coleta.'\n"
        )
    else:
        prompt_final = (
            f"{prompt}\n\n"
            f"Responda de forma clara, direta e fácil de entender, fornecendo orientações sobre reciclagem ou descarte responsável, mesmo que não haja materiais identificados em uma imagem. "
            f"Se a dúvida for geral, explique como separar, armazenar ou lidar com resíduos de maneira segura e higiênica em casa, sem mencionar locais de descarte ou centros de reciclagem.\n\n"
            f"Importante: responda apenas com o texto da orientação. Não use formatação extra, listas, JSON ou estrutura de dicionário. Não adicione explicações fora da mensagem. Apenas o texto direto com as instruções.\n"
        )

    role = "voce é um especialista em reciclagem e meio ambiente. Seu trabalho é fornecer orientações claras e precisas sobre como reciclar ou descartar corretamente os materiais."
    return prompt_final, role

@router.post(
    "/",
    summary="Realizar consulta com o chatbot de reciclagem",
    description="Realiza a consulta com o chatbot de reciclagem.",
    response_description="Retorna uma mensagem com as orientações de reciclagem.",
    responses={
        200: {
            "description": "Resposta bem-sucedida com mensagem de orientação.",
            "content": {
                "application/json": {
                    "example": {
                        "mensagem": "Garrafas PET devem ser lavadas, secas..."
                    }
                }
            },
        },
        400: {
            "description": "Erro na validação dos dados enviados.",
            "content": {
                "application/json": {"example": {"detail": "Formato de imagem não suportado."}}
            },
        },
        500: {
            "description": "Erro interno do servidor.",
            "content": {
                "application/json": {"example": {"detail": "Erro ao processar a solicitação."}}
            },
        },
    },
)
async def post_new_chat(
    prompt: str = Form(...),
    img: UploadFile = File(None),
    db: AsyncSession = Depends(get_session),
):
    try:
        materiais: list[str] = []

        if img is not None:
            conteudo = await img.read()

            if not conteudo:
                img = None  # trata imagem vazia como inexistente
            elif img.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException(status_code=400, detail="Formato de imagem não suportado. Envie JPEG ou PNG.")
            else:
                resultado_classificacao = await classificar_imagem_azure(conteudo)

                predicoes_filtradas = [
                    pred["tagName"]
                    for pred in resultado_classificacao.get("predictions", [])
                    if pred["probability"] > 0.5
                ]

                contagem = Counter(predicoes_filtradas)
                materiais = [nome for nome, _ in contagem.items()]

        # Chamar serviço de linguagem generativa
        prompt_final, role = await gerar_orientacoes_reciclagem(materiais, prompt)
        texto = await gerar_texto(prompt_final, role)

        return {"mensagem": texto}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
