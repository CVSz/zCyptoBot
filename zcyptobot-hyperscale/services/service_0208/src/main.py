from fastapi import FastAPI

app = FastAPI(title='service_0208')

@app.get('/health')
def health():
    return {'service': 'service_0208', 'status': 'ok'}
