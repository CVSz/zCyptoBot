from pydantic import BaseModel


class User(BaseModel):
    username: str
    role: str
    tenant_id: str = "public"
