from fastapi import FastAPI

app = FastAPI(title='service_0101')

@app.get('/health')
def health():
    return {'service': 'service_0101', 'status': 'ok'}
