from app.server.routes import api_router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="campaign_banner", version="0.1.0")

app.mount("/static", StaticFiles(directory="static/images"), name="static")
app.include_router(api_router)
