from fastapi import FastAPI

app = FastAPI(title='service_0020')

@app.get('/health')
def health():
    return {'service': 'service_0020', 'status': 'ok'}
