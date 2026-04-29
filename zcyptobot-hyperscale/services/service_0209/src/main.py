from fastapi import FastAPI

app = FastAPI(title='service_0209')

@app.get('/health')
def health():
    return {'service': 'service_0209', 'status': 'ok'}
