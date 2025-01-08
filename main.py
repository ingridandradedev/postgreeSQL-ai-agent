from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from langchain.agents import initialize_agent, Tool
from langchain_community.chat_models import ChatOpenAI
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from typing import Any, Dict

app = FastAPI()

class QueryRequest(BaseModel):
    input: str
    db_credentials: Dict[str, str]

# Função para executar a query no PostgreSQL
def postgre_sql_query(
    query: str,
    host: str,
    database: str,
    user: str,
    password: str,
    port: int = 5432
) -> Any:
    try:
        conn = connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.post("/query")
def query_agent(
    request: QueryRequest,
    Authorization: str = Header(None)  # <-- Para receber o cabeçalho "Authorization"
):
    try:
        # Extrai o token (OpenAI API Key) do cabeçalho "Authorization: Bearer <chave>"
        if not Authorization:
            raise HTTPException(
                status_code=401,
                detail="Authorization header is missing."
            )
        if not Authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authorization header must start with 'Bearer '."
            )
        openai_api_key = Authorization.split(" ")[1]  # ou Authorization[7:]

        # Extrair credenciais do request
        credentials = request.db_credentials

        # Criar a "ferramenta" (Tool) a partir de uma função
        tool = Tool(
            name="postgre_sql_query",
            func=lambda q: postgre_sql_query(
                q,
                host=credentials["host"],
                database=credentials["database"],
                user=credentials["user"],
                password=credentials["password"],
                port=int(credentials.get("port", 5432))
            ),
            description="Ferramenta para executar consultas em um banco de dados PostgreSQL."
        )

        # Aqui passamos explicitamente o openai_api_key
        llm = ChatOpenAI(
            model="gpt-4-turbo",
            temperature=0.1,
            openai_api_key=openai_api_key  # <-- chave capturada do header
        )

        # Cria o agente com base no LLM e na ferramenta
        agent = initialize_agent(
            tools=[tool],
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True
        )

        # Executa a consulta através do agente
        response = agent.run(request.input)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
