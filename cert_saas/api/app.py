from fastapi import FastAPI

from cert_saas.core.attestation import generate

app = FastAPI()


@app.get("/attestation")
def attest():
    # plug STATE in production
    return generate([])
