from fastapi import FastAPI

app = FastAPI(title='service_0129')

@app.get('/health')
def health():
    return {'service': 'service_0129', 'status': 'ok'}
