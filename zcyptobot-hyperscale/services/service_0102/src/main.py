from fastapi import FastAPI

app = FastAPI(title='service_0102')

@app.get('/health')
def health():
    return {'service': 'service_0102', 'status': 'ok'}
