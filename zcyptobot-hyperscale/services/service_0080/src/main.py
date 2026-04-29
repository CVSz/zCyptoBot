from fastapi import FastAPI

app = FastAPI(title='service_0080')

@app.get('/health')
def health():
    return {'service': 'service_0080', 'status': 'ok'}
