import os
import requests
import google.auth
from google.auth.transport.requests import Request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações extraídas do notebook
PROJECT_ID = "llm-studies"
LOCATION = "global"
AGENT_ID = "events_data_agent"
API_VERSION = "v1beta"
BASE_URL = "https://geminidataanalytics.googleapis.com"

class ChatRequest(BaseModel):
    query: str
    session_id: str # Usado como conversation_id

@app.post("/chat")
async def chat_with_bq_agent(request: ChatRequest):
    try:
        # 1. Autenticação
        creds, _ = google.auth.default()
        creds.refresh(Request())
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }

        conv_id = request.session_id
        
        # 2. Criar ou validar a Conversa
        # No Gemini Data Analytics, a conversa deve apontar para o dataAgent específico
        conv_url = f"{BASE_URL}/{API_VERSION}/projects/{PROJECT_ID}/locations/{LOCATION}/conversations"
        conv_payload = {
            "agents": [
                f"projects/{PROJECT_ID}/locations/{LOCATION}/dataAgents/{AGENT_ID}"
            ],
            "name": f"projects/{PROJECT_ID}/locations/{LOCATION}/conversations/{conv_id}"
        }
        
        # Tenta criar a conversa; se já existir, o serviço geralmente valida ou ignora
        requests.post(conv_url, headers=headers, json=conv_payload, params={"conversation_id": conv_id})

        # 3. Enviar a Mensagem
        msg_url = f"{BASE_URL}/{API_VERSION}/projects/{PROJECT_ID}/locations/{LOCATION}/conversations/{conv_id}/messages:create"
        
        msg_payload = {
            "content": {"text": request.query}
        }

        response = requests.post(msg_url, headers=headers, json=msg_payload)

        if response.status_code != 200:
            raise Exception(f"Erro ao enviar mensagem: {response.text}")

        data = response.json()

        # 4. Retornar a resposta do Agente
        # A estrutura de resposta no notebook indica que o conteúdo textual fica em 'answer' -> 'content'
        return {
            "answer": data.get("answer", {}).get("content", "Sem resposta textual."),
            "session_id": conv_id
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)