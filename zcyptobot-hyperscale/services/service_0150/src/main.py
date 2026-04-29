from fastapi import FastAPI

app = FastAPI(title='service_0150')

@app.get('/health')
def health():
    return {'service': 'service_0150', 'status': 'ok'}
