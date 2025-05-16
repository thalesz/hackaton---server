from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from app.core.base import Base  # Importando o Base correto
from typing import Optional


class MoradorModel(Base, SQLModel, table=True):
    __tablename__ = "morador"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nome: str = Field(sa_column=Column(String(100), nullable=False))
    condominio: int = Field(
        sa_column=Column(Integer, ForeignKey("condominio.id"), nullable=False)
    )


    class Config:
        arbitrary_types_allowed = True