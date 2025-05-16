from pydantic import BaseModel, Field
from app.basic.morador import morador  # Assuming this is the correct import path for your cards
from app.models.morador import MoradorModel

from sqlalchemy import Column, String, Integer, select, ForeignKey
from sqlalchemy.exc import IntegrityError
from app.core.base import Base  # Importando o Base correto
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession


class MoradorSchemaBase(BaseModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        validate_assignment = True

    @staticmethod
    async def get_all_moradores_by_id_condominio(session: AsyncSession, id_condominio: int):
        result = await session.execute(
            select(MoradorModel).where(MoradorModel.condominio == id_condominio)
        )
        moradores = result.scalars().all()
        return moradores
    
    
    @staticmethod
    async def sync_moradores(session: AsyncSession):
        for morador_data in morador:
            result = await session.execute(
                select(MoradorModel).where(MoradorModel.id == morador_data["id"])
            )
            existing = result.scalars().first()

            if not existing:
                new_morador = MoradorModel(
                    id=morador_data["id"],
                    nome=morador_data["nome"], # Alterado de "name" para "nome"
                    condominio=morador_data["condominio"]
                )
                session.add(new_morador)
                try:
                    await session.commit()
                    print(f'Morador "{morador_data["nome"]}" adicionado.')
                except IntegrityError:
                    await session.rollback()
                    print(f'Erro ao adicionar "{morador_data["nome"]}". Conflito de integridade.')
            else:
                print(f'Morador "{morador_data["nome"]}" já existe no banco.')

class MoradorSchema(MoradorSchemaBase):
    id: Optional[int] = Field(
        sa_column=Column(Integer, primary_key=True, autoincrement=True)
    )
    nome: str = Field(
        sa_column=Column(String(100), nullable=False)
    )  # Nome do card
    condominio: int = Field(
        sa_column=Column(Integer, ForeignKey("condominio.id"), nullable=False)
    )  # ID do condominio