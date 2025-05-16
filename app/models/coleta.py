from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import ARRAY
from app.core.base import Base  # Importando o Base correto
from typing import Optional, List


class ColetaModel(Base, SQLModel, table=True):
    __tablename__ = "coleta"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    residuos: List[str]= Field(
        sa_column=Column(MutableList.as_mutable(ARRAY(String)), nullable=True)
    )  
    data: str = Field(sa_column=Column(String(100), nullable=False))  # Data do agendamento
    morador: int = Field(
        sa_column=Column(Integer, ForeignKey("morador.id"), nullable=False)
    )  # Chave estrangeira para o morador
    condominio: int = Field(
        sa_column=Column(Integer, ForeignKey("condominio.id"), nullable=False)
    )  # Chave estrangeira para o condomínio


    class Config:
        arbitrary_types_allowed = True