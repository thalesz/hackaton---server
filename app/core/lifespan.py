from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.postgresdatabase import engine, Session
from app.core.base import Base

# Isso garante que todos os modelos sejam registrados no metadata
from app.models import __all_models  # noqa: F401
from app.models.condominio import CondominioModel
from app.models.morador import MoradorModel
from app.models.coleta import ColetaModel


from app.schemas.condominio import CondominioSchema
from app.schemas.morador import MoradorSchema



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        print("📌 Modelos registrados:")
        for table_name in Base.metadata.tables.keys():
            print(f"➡ {table_name}")

        print("💾 Criando tabelas no banco (se ainda não existirem)...")
        await conn.run_sync(Base.metadata.create_all)

    async with Session() as session:
        db: AsyncSession = session
        await CondominioSchema.sync_condominios(
            session=db
        )
        await MoradorSchema.sync_moradores(session=db)
        print("💾 Tabelas adicionadas!")
    yield
