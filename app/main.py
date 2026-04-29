from fastapi import FastAPI
import asyncio
from app.core.orchestrator import Orchestrator

app = FastAPI()
bot = Orchestrator()


@app.on_event("startup")
async def startup():
    asyncio.create_task(bot.run())


@app.get("/health")
def health():
    return {"status": "ok"}
