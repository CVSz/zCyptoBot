from fastapi import FastAPI

app = FastAPI(title='service_0105')

@app.get('/health')
def health():
    return {'service': 'service_0105', 'status': 'ok'}
