from fastapi import FastAPI

app = FastAPI(title='service_0202')

@app.get('/health')
def health():
    return {'service': 'service_0202', 'status': 'ok'}
