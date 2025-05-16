# 🛠️ Hackathon Project

Bem-vindo ao repositório do projeto **Hackathon**! 🚀

## 📌 Descrição

Este projeto foi desenvolvido durante um hackathon com o objetivo de resolver um desafio real por meio de tecnologia, inovação e impacto social/ambiental. A solução foca em tornar o processo de identificação e orientação sobre descarte de resíduos mais inteligente e acessível, utilizando inteligência artificial e visão computacional.

## ⚙️ Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) – Framework web moderno e rápido (Python 3.7+)
- Python – Linguagem principal da aplicação
- SQLAlchemy – ORM para integração com banco de dados
- Azure Custom Vision – Classificação automática de imagens
- OpenAI / LLM (se aplicável) – Geração de texto para orientações sobre descarte
- PostgreSQL ou SQLite – Banco de dados
- Pydantic – Validação de dados
- Uvicorn – Servidor ASGI para FastAPI

## 🚀 Funcionalidades

- Upload de imagem de resíduos
- Classificação automática dos materiais presentes
- Geração de orientações sobre como armazenar corretamente os materiais até a coleta
- Registro das coletas com vínculo a moradores e condomínios
- API RESTful com endpoints seguros e prontos para integração

## 🔧 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo-hackathon.git
   cd seu-repo-hackathon
   ```

2. Crie e ative seu ambiente virtual 

  ```bash
  python -m venv venv
  source venv/bin/activate  # ou venv\Scripts\activate no Windows
  ```

3. Instale os requisitos

  ```bash
  pip install -r requirements.txt
  ```

4. Inicie o servidor 

  ```bash
 uvicorn app.main:app  
  ```