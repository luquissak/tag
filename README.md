
# Getting Stated

```bash
mkdir hello-world-firebase
cd hello-world-firebase
npm install -g firebase-tools
firebase login
firebase init hosting
```

# Firebase

```bash
firebase serve
firebase open
firebase console
```


Step 1: Set up a Firebase Project and Enable Analytics 
Step 2: Add the Analytics SDK to Your App 



3. Create venv
```bash
py -m venv .venv
.venv\scripts\activate
.venv\scripts\python -m pip install --upgrade pip
.venv\scripts\activate && .venv\Scripts\pip install -r requirements.txt
```

.venv\scripts\activate && .venv\Scripts\python data_agent\create_end.py

pip install requests

gcloud auth login
gcloud auth application-default login

# Load var
```bash
get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
    echo $name $value
}
```
# Acesso

- [Console Firebase](https://console.firebase.google.com/project/llm-studies/overview)
- [Google Analytics Console](https://analytics.google.com/analytics/web/?hl=pt-br#/a134714060p527405664/reports/intelligenthome)
- [App Hello World!](https://llm-studies.web.app/)

https://share.google/aimode/9l7lAq8mgEjP0j6Q5
https://firebase.google.com/docs/samples?hl=pt-br
https://firebase.google.com/docs/web/setup?hl=pt-br
https://firebase.google.com/docs/hosting?hl=pt-br
https://tagmanager.google.com/#/home
https://marketingplatform.google.com/home?utm_campaign=SuiteHeader&utm_source=UniversalPicker&utm_medium=platformHomeButton&authuser=0
https://gemini.google.com/app/ddfcd7733f9f9759?hl=pt-BR
https://analytics.google.com/analytics/web/?hl=pt-br#/a134714060p527405664/reports/intelligenthome
https://support.google.com/analytics/answer/9289234
https://support.google.com/analytics/answer/9304153?hl=pt-BR&utm_id=ad#setup-datacollection
https://cloud.google.com/bigquery/pricing?hl=pt-BR&authuser=0




gcloud auth print-identity-token --audiences=https://geminidataanalytics.googleapis.com


gcloud auth print-identity-token --audiences=https://geminidataanalytics.googleapis.com


curl  -H "Authorization: Bearer $(gcloud auth print-identity-token)" https://geminidataanalytics.googleapis.com/

# 1. Obter o token e salvar na variável $token
$token = gcloud auth print-identity-token

# 2. Fazer a chamada usando Invoke-RestMethod (mais limpo que o Invoke-WebRequest)
Invoke-RestMethod -Uri "https://geminidataanalytics.googleapis.com" -Method Get -Headers @{ Authorization = "Bearer $token" }


$location=us-central1
$token = gcloud auth print-identity-token
$token = gcloud auth print-access-token

set-content env:project llm-studies
ls Env:project
set-content env:location us-central1
ls Env:location
set-content env:token (gcloud auth print-access-token)
$Env:token


set-content env:url https://geminidataanalytics.googleapis.com/v1/projects/$Env:project/locations/$Env:location/operations
ls Env:url

Invoke-RestMethod -Uri $Env:url -Method Get -Headers @{ Authorization = "Bearer $Env:token" }

gcloud services enable geminidataanalytics.googleapis.com --project llm-studies
gcloud auth application-default login



jupyter notebook


chrome pessoal lquissakn

https://crimson-comet-700387.postman.co/workspace/f7909bd4-527f-4cea-ad8c-53f2e602d80f/request/4066046-29586f49-0231-4a45-8442-e30c7bdca8ba?tab=auth

