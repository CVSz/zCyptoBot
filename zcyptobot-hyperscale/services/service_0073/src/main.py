from fastapi import FastAPI

app = FastAPI(title='service_0073')

@app.get('/health')
def health():
    return {'service': 'service_0073', 'status': 'ok'}
