from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_session
from app.schemas.morador import MoradorSchemaBase
from app.schemas.coleta import ColetaSchemaBase
from app.services.computevision import classificar_imagem_azure
from app.services.openai import gerar_texto
from datetime import datetime
import re
import json

router = APIRouter()

# Supondo que você tenha uma função de linguagem generativa
async def gerar_orientacoes_reciclagem(materiais: list[str], prompt: str) -> str:
    materiais_texto = ", ".join(materiais)
    prompt_final = (
        f"{prompt}\n\n"
        f"Foram detectados os seguintes materiais na imagem: {materiais_texto}.\n\n"
        f"Com base nesses materiais, escreva um texto claro, direto e fácil de entender, explicando como a pessoa deve armazenar corretamente cada um deles até que o serviço de coleta passe para retirar. "
        f"Não mencione locais de descarte nem centros de reciclagem — só diga como guardar de forma segura, higiênica e responsável dentro de casa.\n\n"
        f"Importante: responda apenas com o texto da orientação. Não use formatação extra, listas, JSON ou estrutura de dicionário. Não adicione explicações fora da mensagem. Apenas o texto direto com as instruções.\n"
        f"Exemplo de resposta: 'Garrafas PET devem ser lavadas, secas e armazenadas em sacos plásticos transparentes. Caixas de papelão podem ser desmontadas e mantidas em local seco até a coleta.'\n"
    )

    role = "voce de um especialista em reciclagem e meio ambiente. seu trabalho é fornecer orientações claras e precisas sobre como reciclar ou descartar corretamente os materiais."
    return prompt_final, role 

def extract_json_from_reading(reading):
    regex = r'```json\s*([\s\S]*?)\s*```'
    match = re.search(regex, reading)
    if match and match.group(1):
        try:
            json_data = json.loads(match.group(1))
            return json_data
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
    return None


@router.post(
    "/",
    summary="Realizar consulta com o chatbot de reciclagem",
    description="Realiza a consulta com o chatbot de reciclagem.",
    response_description="retorna uma mensagem com as orientações de reciclagem.",
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

    
async def post_new_chat(
    prompt: str = Form(...),
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

        # Extrair apenas os nomes dos materiais para passar para a função de orientação
        materiais = [item["nome"] for item in resposta_final]

        # chamar o servico de linguagem generativa
        orientacoes, role  = await gerar_orientacoes_reciclagem(materiais, prompt)
        
        texto = await gerar_texto(orientacoes, role)
        print("Texto gerado:", texto)   
        # texto = extract_json_from_reading(texto)
        
        return {
            "mensagem": texto
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
