from fastapi import FastAPI

app = FastAPI(title='service_0097')

@app.get('/health')
def health():
    return {'service': 'service_0097', 'status': 'ok'}
