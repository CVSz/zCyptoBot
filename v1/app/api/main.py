from fastapi import FastAPI

from app.api.routes_admin import router as admin
from app.api.routes_auth import router as auth
from app.api.routes_god import router as god
from app.api.routes_aiops import router as aiops
from app.api.routes_user import router as user
from app.tenancy.middleware import TenantMiddleware

app = FastAPI(title="ZEAZ v2 SaaS")
app.add_middleware(TenantMiddleware)

app.include_router(auth, prefix="/auth")
app.include_router(user, prefix="/user")
app.include_router(admin, prefix="/admin")
app.include_router(god, prefix="/god")

app.include_router(aiops, prefix='/aiops')
