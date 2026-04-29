from fastapi import FastAPI

app = FastAPI(title='service_0002')

@app.get('/health')
def health():
    return {'service': 'service_0002', 'status': 'ok'}
