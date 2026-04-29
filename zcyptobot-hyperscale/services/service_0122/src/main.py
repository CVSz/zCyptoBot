from fastapi import FastAPI

app = FastAPI(title='service_0122')

@app.get('/health')
def health():
    return {'service': 'service_0122', 'status': 'ok'}
