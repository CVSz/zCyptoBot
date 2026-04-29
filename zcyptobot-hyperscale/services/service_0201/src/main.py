from fastapi import FastAPI

app = FastAPI(title='service_0201')

@app.get('/health')
def health():
    return {'service': 'service_0201', 'status': 'ok'}
