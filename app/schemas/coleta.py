from pydantic import BaseModel, Field
from app.models.coleta import ColetaModel
from sqlalchemy import select

class ColetaSchemaBase(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        validate_assignment = True
        
    @staticmethod
    async def retornar_coletas(session, morador: int, condominio: int):
        try:
            stmt = select(ColetaModel).where(
                ColetaModel.morador == morador,
                ColetaModel.condominio == condominio
            )
            result = await session.execute(stmt)
            coletas = result.scalars().all()
            print("coletas:", coletas)  # Deve agora mostrar lista de objetos ColetaModel
            return coletas
        except Exception as e:
            raise RuntimeError(f"Erro ao buscar coletas: {e}")

        
    @staticmethod
    async def criar_coleta(session, residuos: list[str], data: str, morador: int, condominio: int):
        try:
            # Convert datetime to string if necessary
            if hasattr(data, "isoformat"):
                data_str = data.isoformat()
            else:
                data_str = data
            nova_coleta = ColetaModel(
                residuos=residuos,
                data=data_str,
                morador=morador,
                condominio=condominio
            )

            session.add(nova_coleta)
            await session.commit()
            await session.refresh(nova_coleta)

            return nova_coleta
        except Exception as e:
            await session.rollback()
            raise RuntimeError(f"Erro ao criar coleta: {e}")
        

class ColetaSchema(ColetaSchemaBase):
    id: int = Field(default=None, primary_key=True, index=True)
    residuos: list[str] = Field(default=None, nullable=True)
    data: str = Field(default=None, nullable=False)  # Data do agendamento
    morador: int = Field(default=None, nullable=False)  # Chave estrangeira para o morador
    condominio: int = Field(default=None, nullable=False)  # Chave estrangeira para o condomínio
    