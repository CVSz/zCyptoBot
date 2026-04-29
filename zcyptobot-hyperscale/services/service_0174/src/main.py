from fastapi import FastAPI

app = FastAPI(title='service_0174')

@app.get('/health')
def health():
    return {'service': 'service_0174', 'status': 'ok'}
