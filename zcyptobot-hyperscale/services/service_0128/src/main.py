from fastapi import FastAPI

app = FastAPI(title='service_0128')

@app.get('/health')
def health():
    return {'service': 'service_0128', 'status': 'ok'}
