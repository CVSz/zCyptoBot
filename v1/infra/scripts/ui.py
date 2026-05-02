from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, status
import os
import subprocess
from pathlib import Path
import logging

app = FastAPI()
logger = logging.getLogger(__name__)

# Require a deploy token to prevent unauthenticated execution of deployment scripts.
# Set DEPLOY_TOKEN in the environment in production. If unset, deployment is disabled.
DEPLOY_TOKEN = os.getenv("DEPLOY_TOKEN")


def _run_deploy_script():
    script = Path("infra/scripts/deploy.sh")
    if not script.exists():
        logger.error("Deploy script not found: %s", script)
        return
    # Execute the script without using the shell to avoid shell injection.
    try:
        subprocess.run(["/bin/bash", str(script)], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=str(script.parent))
    except Exception as e:
        logger.exception("Deploy script execution failed: %s", e)


@app.post("/deploy")
def deploy(background_tasks: BackgroundTasks, x_deploy_token: str = Header(None)):
    # Validate token if configured. If the token is not set in the environment,
    # deployments are disabled by default.
    if DEPLOY_TOKEN:
        if x_deploy_token != DEPLOY_TOKEN:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    else:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Deploy not configured")

    background_tasks.add_task(_run_deploy_script)
    return {"status": "started"}


@app.get("/status")
def status():
    return {"k8s": "running"}
