from fastapi import FastAPI

app = FastAPI(title='service_0123')

@app.get('/health')
def health():
    return {'service': 'service_0123', 'status': 'ok'}
