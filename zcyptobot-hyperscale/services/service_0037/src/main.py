from fastapi import FastAPI

app = FastAPI(title='service_0037')

@app.get('/health')
def health():
    return {'service': 'service_0037', 'status': 'ok'}
