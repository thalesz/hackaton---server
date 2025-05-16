import httpx
from app.core.configs import settings


async def classificar_imagem_azure(imagem_bytes: bytes) -> dict:
    headers = {
        "Prediction-Key": settings.PREDICTION_KEY,
        "Content-Type": "application/octet-stream"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=settings.PREDICTION_URL,
            headers=headers,
            content=imagem_bytes
        )

    if response.status_code != 200:
        raise Exception(f"Erro ao chamar Azure Prediction API: {response.status_code} - {response.text}")

    return response.json()
