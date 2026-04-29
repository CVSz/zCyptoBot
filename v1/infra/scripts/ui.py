from fastapi import FastAPI
import subprocess

app = FastAPI()


@app.get("/deploy")
def deploy():
    subprocess.Popen(["bash", "infra/scripts/deploy.sh"])
    return {"status": "started"}


@app.get("/status")
def status():
    return {"k8s": "running"}
