from fastapi import FastAPI

app = FastAPI(title='service_0214')

@app.get('/health')
def health():
    return {'service': 'service_0214', 'status': 'ok'}
