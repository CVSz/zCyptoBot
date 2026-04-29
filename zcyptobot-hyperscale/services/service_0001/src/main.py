from fastapi import FastAPI

app = FastAPI(title='service_0001')

@app.get('/health')
def health():
    return {'service': 'service_0001', 'status': 'ok'}
