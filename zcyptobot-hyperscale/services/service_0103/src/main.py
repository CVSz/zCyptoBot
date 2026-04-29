from fastapi import FastAPI

app = FastAPI(title='service_0103')

@app.get('/health')
def health():
    return {'service': 'service_0103', 'status': 'ok'}
