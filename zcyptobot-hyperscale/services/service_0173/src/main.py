from fastapi import FastAPI

app = FastAPI(title='service_0173')

@app.get('/health')
def health():
    return {'service': 'service_0173', 'status': 'ok'}
