import os
import requests
import json
import google.auth
import google.auth.transport.requests
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

def get_google_auth_token():
    credentials, project = google.auth.default(
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    auth_request = google.auth.transport.requests.Request()
    credentials.refresh(auth_request)
    return credentials.token

def create_data_agent():
    # Recuperando variáveis de ambiente
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION")
    agent_id = os.getenv("DATA_AGENT_ID")
    bq_table_uri = os.getenv("BQ_TABLE_URI")

    print(project_id, location, agent_id, bq_table_uri)

    token = get_google_auth_token()
    if not token: return

    url = f"https://conversationalanalytics.googleapis.com/v1alpha1/projects/{project_id}/locations/{location}/dataAgents:createSync"
    
    # Tente a v1 ou v1beta se a v1alpha1 falhar com 404
    url = f"https://conversationalanalytics.googleapis.com/v1/projects/{project_id}/locations/{location}/dataAgents:createSync"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    payload = {
        "dataAgentId": agent_id,
        "dataAgent": {
            "displayName": f"Agente {agent_id}",
            "dataSources": [{"bigquerySource": {"tableUri": bq_table_uri}}],
            "instruction": {"systemInstruction": "Você é um analista de dados."}
        }
    }

    print(f"🚀 Enviando requisição para {location}...")
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)

if __name__ == "__main__":
    create_data_agent()