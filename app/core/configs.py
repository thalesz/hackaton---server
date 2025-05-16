from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    POSTGRES_URL: str
    PREDICTION_URL: str
    PREDICTION_KEY: str
    AZURE_API_KEY: str
    AZURE_ENDPOINT: str

    class Config:
        env_file = ".env"  # Arquivo de onde as variáveis serão carregadas
        extra = "ignore"  # Ignora variáveis extras no .env que não estão definidas aqui
        case_sensitive = True

settings: Settings = Settings()
