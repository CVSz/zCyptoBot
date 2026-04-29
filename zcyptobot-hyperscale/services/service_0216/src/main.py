from fastapi import FastAPI

app = FastAPI(title='service_0216')

@app.get('/health')
def health():
    return {'service': 'service_0216', 'status': 'ok'}
