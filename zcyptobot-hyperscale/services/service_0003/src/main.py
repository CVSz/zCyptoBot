from fastapi import FastAPI

app = FastAPI(title='service_0003')

@app.get('/health')
def health():
    return {'service': 'service_0003', 'status': 'ok'}
