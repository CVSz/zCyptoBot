from fastapi import FastAPI

app = FastAPI(title='service_0207')

@app.get('/health')
def health():
    return {'service': 'service_0207', 'status': 'ok'}
