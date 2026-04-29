from fastapi import FastAPI

app = FastAPI(title='service_0004')

@app.get('/health')
def health():
    return {'service': 'service_0004', 'status': 'ok'}
