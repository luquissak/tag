# TPU

Zonas SA

```bash
gcloud services enable tpu.googleapis.com --project=llm-studies
gcloud projects add-iam-policy-binding llm-studies --member="user:lquissakng@gmail.com" --role="roles/tpu.admin"
gcloud compute tpus accelerator-types list --zone=southamerica-east1-a
gcloud compute tpus accelerator-types list --zone=southamerica-east1-b
gcloud compute tpus accelerator-types list --zone=southamerica-east1-c
#gcloud compute project-info describe --project=llm-studies --format="yaml(quotas)"

```

```bash
$Env:SA_EMAIL="$Env:SA_NAME@$Env:GCP_PROJECT_ID.iam.gserviceaccount.com"
$Env:SA_EMAIL
gcloud iam service-accounts create $Env:SA_NAME --description="Service Account para gerenciar e subir TPUs via GKE/DWS" --display-name="TPU Manager SA" --project=$Env:GCP_PROJECT_ID
gcloud projects add-iam-policy-binding $Env:GCP_PROJECT_ID --member="serviceAccount:$Env:SA_EMAIL" --role="roles/tpu.admin"
gcloud projects add-iam-policy-binding $Env:GCP_PROJECT_ID --member="serviceAccount:$Env:SA_EMAIL" --role="roles/iam.serviceAccountUser"
gcloud iam service-accounts keys create ./tpu-sa-key.json  --iam-account=$Env:SA_EMAIL --project=$GCP_PROJECT_ID
```

```bash
$Env:SA_EMAIL="$Env:SA_NAME@$Env:GCP_PROJECT_ID.iam.gserviceaccount.com"
gcloud alpha compute tpus queued-resources create tpu-test-sku-v6e-1h --node-id=tpu-v6e-sae1-test --zone=$Env:ZONE --accelerator-type=v6e-1 --runtime-version=v2-alpha-tpuv6e --provisioning-model=flex-start --max-run-duration=1h --network=default --subnetwork=default --internal-ips --service-account=$Env:SA_EMAIL --project=$Env:GCP_PROJECT_ID


gcloud beta container node-pools create tpu-pool \
    --project damadei-argolis-h1-26 \
    --cluster sae1-tpu-cluster \
    --region southamerica-east1-c \
    --node-version "1.34.4-gke.1047000" \
    --machine-type "ct6e-standard-1t" \
    --image-type "COS_CONTAINERD" \
    --disk-type "hyperdisk-balanced" \
    --disk-size "200" \
    --service-account "gce-editor@damadei-argolis-h1-26.iam.gserviceaccount.com" \
    --flex-start \
    --enable-autoscaling \
    --num-nodes 0 \
    --min-nodes 0 \
    --max-nodes 1 \
    --location-policy ANY \
    --enable-private-nodes \
    --enable-autoupgrade \
    --enable-autorepair \
    --reservation-affinity=none \
    --max-surge-upgrade 1 \
    --max-unavailable-upgrade 0 \
    --shielded-integrity-monitoring \
    --no-shielded-secure-boot

gcloud alpha compute tpus queued-resources describe tpu-test-sku-v6e-1h --zone=$Env:ZONE --project=$Env:GCP_PROJECT_ID



gcloud beta compute regions describe southamerica-east1 --project=$Env:GCP_PROJECT_ID  --format="table(quotas.metric, quotas.limit, quotas.usage)" | grep TPU
gcloud beta compute regions describe southamerica-east1 --project=$Env:GCP_PROJECT_ID --format="json" | ConvertFrom-Json | Select-Object -ExpandProperty quotas | Where-Object { $_.metric -like "*TPU*" }


# Para checar no outro projeto rapidamente:
gcloud alpha services quota list --project=$Env:GCP_PROJECT_ID --service="tpu.googleapis.com" --regions="southamerica-east1"
```

gcloud compute regions describe southamerica-east1 --project=$Env:GCP*PROJECT_ID --format="json" | ConvertFrom-Json | Select-Object -ExpandProperty quotas | Where-Object { $*.metric -like "_TPU_" }

# Cluster GKE

1. Criar o cluster

```bash
gcloud container clusters create meu-cluster-aprendizado `
    --project $Env:GCP_PROJECT_ID `
    --region $Env:GCP_LOCATION  `
    --num-nodes 1  `
    --machine-type e2-micro  `
    --spot  `
    --disk-size 15  `
    --no-enable-cloud-logging  `
    --no-enable-cloud-monitoring
```

```bash
gcloud container clusters delete meu-cluster-aprendizado --region us-central1
```

```bash
    --zone $Env:ZONE `
    --network "caixa-south-america-test" `
    --subnetwork "subnet-caixa-south-america" `
    --workload-pool "$Env:GCP_PROJECT_ID.svc.id.goog" `
    --enable-ip-alias
```

```bash
kubectl get nodes
kubectl describe node | findstr /C:"Allocatable" /C:"Capacity"
kubectl describe nodes | select-string "Allocatable" -Context 0,5
gcloud container clusters resize meu-cluster-aprendizado --num-nodes=0 --region $Env:GCP_LOCATION --node-pool default-pool
kubectl get nodes
gcloud container clusters resize meu-cluster-aprendizado --num-nodes=1 --region $Env:GCP_LOCATION --node-pool default-pool
kubectl get nodes
kubectl run nginx-teste --image=nginx --port=80
```
