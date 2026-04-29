from fastapi import FastAPI

app = FastAPI(title='service_0087')

@app.get('/health')
def health():
    return {'service': 'service_0087', 'status': 'ok'}
