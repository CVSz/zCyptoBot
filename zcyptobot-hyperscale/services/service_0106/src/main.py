from fastapi import FastAPI

app = FastAPI(title='service_0106')

@app.get('/health')
def health():
    return {'service': 'service_0106', 'status': 'ok'}
