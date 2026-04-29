from fastapi import FastAPI

app = FastAPI(title='service_0121')

@app.get('/health')
def health():
    return {'service': 'service_0121', 'status': 'ok'}
