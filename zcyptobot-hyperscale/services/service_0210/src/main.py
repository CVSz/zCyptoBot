from fastapi import FastAPI

app = FastAPI(title='service_0210')

@app.get('/health')
def health():
    return {'service': 'service_0210', 'status': 'ok'}
