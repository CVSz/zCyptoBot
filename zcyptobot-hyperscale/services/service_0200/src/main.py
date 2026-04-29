from fastapi import FastAPI

app = FastAPI(title='service_0200')

@app.get('/health')
def health():
    return {'service': 'service_0200', 'status': 'ok'}
