from fastapi import FastAPI

app = FastAPI(title='service_0206')

@app.get('/health')
def health():
    return {'service': 'service_0206', 'status': 'ok'}
