import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.cloud import discoveryengine_v1beta as discoveryengine


project = os.getenv("GCP_PROJECT_ID") 
print(f"Project ID: {project}")
GCP_LOCATION = os.getenv("LOCATION", "us-central1")
location = os.getenv("LOCATION", "us-central1")
print(f"Location: {location}")

agent = os.getenv("AGENT_ID")
print(f"Agent ID: {agent}")

data_store = os.getenv("DATA_STORE_ID")
print(f"Data Store ID: {data_store}")

app = FastAPI(title="Vertex Agent Bridge")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000"], # Onde o seu Firebase está rodando
    allow_credentials=True,
    allow_methods=["*"], # Permite POST, GET, etc.
    allow_headers=["*"], # Permite X-Firebase-AppCheck, Content-Type, etc.
)

# Modelo de dados para a requisição
class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session"

@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    try:
        # 1. Inicializa o cliente do Discovery Engine
        client = discoveryengine.ConversationalSearchServiceClient()

        # 2. Configura o caminho do Agent Engine / Data Store
        # No Vertex Agent Builder, o 'serving_config' padrão geralmente é 'default_serving_config'
        serving_config = client.serving_config_path(
            project=project,
            location=location,
            data_store=data_store,
            serving_config="default_serving_config"
        )

        # 3. Prepara a consulta
        query_input = discoveryengine.Query(text_input=request.query)
        
        # 4. Chama a API do Vertex
        # Nota: 'answer_query' é ideal para agentes de busca/RAG
        response = client.answer_query(
            discoveryengine.AnswerQueryRequest(
                serving_config=serving_config,
                query=query_input,
                session_id=request.session_id # Mantém o histórico da conversa
            )
        )

        # 5. Retorna a resposta limpa
        return {
            "answer": response.answer.answer_text,
            "session_id": response.session_id,
            "citations": [source.title for source in response.answer.citations]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)