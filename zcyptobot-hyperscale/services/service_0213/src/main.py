from fastapi import FastAPI

app = FastAPI(title='service_0213')

@app.get('/health')
def health():
    return {'service': 'service_0213', 'status': 'ok'}
