import os

import requests
import subprocess
import json
from dotenv import load_dotenv

def get_google_auth_token():
    """Obtém o token de acesso via gcloud CLI."""
    try:
        token = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"], 
            encoding="utf-8"
        ).strip()
        return token
    except Exception as e:
        print(f"Erro ao obter token: {e}")
        return None

def create_data_agent(project_id, location, agent_id, bq_table_uri):
    token = get_google_auth_token()
    if not token:
        return

    url = f"https://conversationalanalytics.googleapis.com/v1alpha1/projects/{project_id}/locations/{location}/dataAgents:createSync"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    # Estrutura do Data Agent
    payload = {
        "dataAgentId": agent_id,
        "dataAgent": {
            "displayName": "Agente de Analytics Inteligente",
            "description": "Agente para consultas em linguagem natural sobre BigQuery",
            "dataSources": [
                {
                    "bigquerySource": {
                        "tableUri": bq_table_uri
                    }
                }
            ],
            "instruction": {
                "systemInstruction": "Você é um assistente de dados. Responda perguntas baseadas apenas nos dados fornecidos."
            }
        }
    }

    print(f"Criando agente '{agent_id}'...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("✅ Sucesso! Agente criado com os seguintes detalhes:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Erro {response.status_code}:")
        print(response.text)

if __name__ == "__main__":
    print
    project_id = os.getenv("GCP_PROJECT_ID")
    location = os.getenv("GCP_LOCATION")
    agent_id = os.getenv("DATA_AGENT_ID")
    bq_table_uri = os.getenv("BQ_TABLE_URI")
    PROJECT_ID = project_id
    LOCATION = location
    AGENT_ID = agent_id
    # Formato: bq://projeto.dataset.tabela
    TABLE_URI = bq_table_uri

    create_data_agent(PROJECT_ID, LOCATION, AGENT_ID, TABLE_URI)