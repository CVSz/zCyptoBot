from fastapi import FastAPI

app = FastAPI(title='service_0204')

@app.get('/health')
def health():
    return {'service': 'service_0204', 'status': 'ok'}
