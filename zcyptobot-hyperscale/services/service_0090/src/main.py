from fastapi import FastAPI

app = FastAPI(title='service_0090')

@app.get('/health')
def health():
    return {'service': 'service_0090', 'status': 'ok'}
