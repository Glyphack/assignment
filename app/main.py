from fastapi import FastAPI

from app.server.routes import api_router

app = FastAPI(title="campaign_banner", version="0.1.0")

app.include_router(api_router)
