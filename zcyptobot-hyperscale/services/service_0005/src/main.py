from fastapi import FastAPI

app = FastAPI(title='service_0005')

@app.get('/health')
def health():
    return {'service': 'service_0005', 'status': 'ok'}
