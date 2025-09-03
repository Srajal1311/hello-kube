📦 Hello-Kube

Tiny Python (Flask) service packaged with Docker, deployed to Kubernetes (Minikube).
Includes liveness/readiness probes, ConfigMap-driven config, and a GitHub Actions → DockerHub CI/CD pipeline.

🚀 Features

1. Python Flask API containerized with Docker
2. Kubernetes Deployment + Service
3. HTTP liveness (/healthz) and readiness (/ready) probes
4. ConfigMap for runtime configuration (/config endpoint)
5. Self-healing (pods auto-restart if killed)
6. Horizontal scaling (via kubectl scale)
7. CI/CD: GitHub Actions builds + pushes to DockerHub on every commit

Deployment helper scripts (deploy.ps1, deploy-latest.ps1)

📁 Project Structure
hello-kube/
├─ app.py
├─ requirements.txt
├─ Dockerfile
├─ k8s/
│  ├─ configmap.yaml
│  ├─ deployment.yaml
│  └─ service.yaml
├─ scripts/
│  ├─ deploy.ps1
│  └─ deploy-latest.ps1
└─ .github/workflows/
   └─ docker-build-push.yml

⚡ Quickstart
1) Run locally with Docker
docker build -t hello-kube:local .
docker run --rm -p 8080:8080 hello-kube:local
# Open http://localhost:8080, /healthz, /ready, /config

2) Deploy to Minikube
minikube start --driver=docker
minikube image load hello-kube:local
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods -l app=hello-kube

3) Access the service

Option A: port-forward

kubectl port-forward svc/hello-kube-service 8080:80

→ then visit http://localhost:8080/config

Option B: NodePort via Minikube

minikube service hello-kube-service

🔧 ConfigMap Demo (change config without rebuild)
kubectl patch configmap hello-config --type merge -p="{\"data\":{\"APP_MESSAGE\":\"Updated via kubectl\"}}"
kubectl rollout restart deploy/hello-kube

Verify:

Invoke-WebRequest http://localhost:8080/config | Select-Object -ExpandProperty Content
# {"APP_MESSAGE":"Updated via kubectl"}

☁️ CI/CD (GitHub Actions → DockerHub)

Every push to main builds and pushes:

1. docker.io/srajal13/hello-kube:<commit-sha>

2. docker.io/srajal13/hello-kube:latest

Deploy pinned commit
powershell -ExecutionPolicy Bypass -File .\scripts\deploy.ps1

Deploy latest
powershell -ExecutionPolicy Bypass -File .\scripts\deploy-latest.ps1

🧪 Demo

1. kubectl get pods -l app=hello-kube → show replicas.
2. Open /config → show ConfigMap value.
3. Patch ConfigMap → refresh /config.
4. Delete a pod → show Kubernetes self-healing.
5. kubectl scale deploy/hello-kube --replicas=3 → show scaling.
6. Show GitHub Actions workflow → DockerHub image pushed automatically.
