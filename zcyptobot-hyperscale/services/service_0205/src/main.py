from fastapi import FastAPI

app = FastAPI(title='service_0205')

@app.get('/health')
def health():
    return {'service': 'service_0205', 'status': 'ok'}
