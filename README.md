# TAG

Firebase App integrated with Big Query and Conversational Analytics Agent

# Clone

```bash
git clone git@github.com:luquissak/tag.git
```

# Create venv

```bash
py -m venv .venv
.venv\scripts\activate
.venv\scripts\python -m pip install --upgrade pip
.venv\scripts\activate && .venv\Scripts\pip install -r requirements.txt
```

```bash
python -m pip install fastapi uvicorn google-cloud-discoveryengine
```

# Load var

```bash
get-content .env | foreach {
    $name, $value = $_.split('=')
    set-content env:\$name $value
    echo $name $value
}
```

# Login

```bash
gcloud auth login lquissakng@gmail.com --force
gcloud auth application-default login lquissakng@gmail.com --billing-project=$Env:GCP_PROJECT_ID
gcloud config set project $Env:GCP_PROJECT_ID
gcloud auth application-default set-quota-project $Env:GCP_PROJECT_ID
gcloud config set billing/quota_project $Env:GCP_PROJECT_ID
gcloud components install beta
gcloud components update
```

# Build

```bash
.venv\scripts\activate
python main.py
jupyter notebook
```

# Acesso

- [Console Firebase](https://console.firebase.google.com/project/llm-studies/overview)
- [Google Analytics Console](https://analytics.google.com/analytics/web/?hl=pt-br#/a134714060p527405664/reports/intelligenthome)
- [App Hello World!](https://llm-studies.web.app/)
- [reCAPTCHA - setup](https://www.google.com/recaptcha/admin/create?hl=pt-br)
- [reCAPTCHA - settings](https://www.google.com/recaptcha/admin/site/748216996/settings?hl=pt-br)
- [reCAPTCHA - console GCP](https://console.cloud.google.com/security/recaptcha?authuser=0&project=llm-studies)


# Getting Stated - Firebase

```bash
mkdir hello-world-firebase
cd hello-world-firebase
npm install -g firebase-tools
firebase login
firebase init hosting
```

# Firebase - commands

```bash
cd hello-world-firebase
firebase serve
firebase open
firebase console
```