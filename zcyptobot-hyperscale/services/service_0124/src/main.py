from fastapi import FastAPI

app = FastAPI(title='service_0124')

@app.get('/health')
def health():
    return {'service': 'service_0124', 'status': 'ok'}
