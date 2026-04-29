from fastapi import FastAPI

app = FastAPI(title='service_0108')

@app.get('/health')
def health():
    return {'service': 'service_0108', 'status': 'ok'}
