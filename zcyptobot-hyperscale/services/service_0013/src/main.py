from fastapi import FastAPI

app = FastAPI(title='service_0013')

@app.get('/health')
def health():
    return {'service': 'service_0013', 'status': 'ok'}
