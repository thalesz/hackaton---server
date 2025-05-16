from pydantic import BaseModel, Field
from app.basic.condominio import condominio  # Assuming this is the correct import path for your cards
from app.models.condominio import CondominioModel

from sqlalchemy import Column, String, Integer, select
from sqlalchemy.exc import IntegrityError
from app.core.base import Base  # Importando o Base correto
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession


class CondominioSchemaBase(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        validate_assignment = True
        
    @staticmethod
    async def get_all_decks(session: AsyncSession):
        result = await session.execute(
            select(CondominioModel)
        )
        decks = result.scalars().all()
        return decks

    @staticmethod
    async def sync_condominios(session: AsyncSession):
        for condominio_data in condominio:
            result = await session.execute(
                select(CondominioModel).where(CondominioModel.id == condominio_data["id"])
            )
            existing = result.scalars().first()

            if not existing:
                new_condominio = CondominioModel(
                    id=condominio_data["id"],
                    nome=condominio_data["nome"]
                )
                session.add(new_condominio)
                try:
                    await session.commit()
                    print(f'Condomínio "{condominio_data["nome"]}" adicionado.')
                except IntegrityError:
                    await session.rollback()
                    print(f'Erro ao adicionar "{condominio_data["nome"]}". Conflito de integridade.')
            else:
                print(f'Condomínio "{condominio_data["nome"]}" já existe no banco.')

class CondominioSchema(CondominioSchemaBase):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )
    nome: str = Field(
        sa_column=Column(String(100), nullable=False)
    )  # Nome do card