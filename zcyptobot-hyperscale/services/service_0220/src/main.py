from fastapi import FastAPI

app = FastAPI(title='service_0220')

@app.get('/health')
def health():
    return {'service': 'service_0220', 'status': 'ok'}
