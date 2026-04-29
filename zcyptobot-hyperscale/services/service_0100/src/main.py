from fastapi import FastAPI

app = FastAPI(title='service_0100')

@app.get('/health')
def health():
    return {'service': 'service_0100', 'status': 'ok'}
