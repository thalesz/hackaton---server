from openai import AzureOpenAI
import os
from dotenv import load_dotenv

from app.core.configs import settings

load_dotenv()

client = AzureOpenAI(
    api_key=settings.AZURE_API_KEY,
    api_version="2023-03-15-preview",
    azure_endpoint=settings.AZURE_ENDPOINT,
)

# prompt_ajustado = os.getenv("PROMPT_AJUSTADO")
# role = os.getenv("ROLE")


# Receber role e prompt por parametro
async def gerar_texto(prompt_ajustado:str, role:str) -> str:
    try:
        # prompt_ajustado = (
        #     f"Escreva um tweet bem polêmico e controverso sobre um tema específico. "
        #     "O texto deve parecer espontâneo, direto e impulsivo – como se alguém estivesse desabafando ou provocando mesmo. "
        #     "Nada de tom robótico ou linguagem formal. Sem emojis, hashtags ou aspas. "
        #     "Tem que cutucar, causar reação, gerar discussão. Nada neutro ou tímido – é pra dividir opiniões e chamar atenção de verdade."
        #      )

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ou o nome do deployment no Azure, como "gpt-35-turbo"
            messages=[
            {"role": "system", "content": role},
            {"role": "user", "content": prompt_ajustado}
            ],
            max_tokens=1400,  # Limite de caracteres para um tweet (280 caracteres)
            temperature=0.9
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar texto: {str(e)}"


