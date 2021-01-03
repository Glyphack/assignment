from fastapi import APIRouter

from app.server.endpoints import campaign

api_router = APIRouter()
api_router.include_router(campaign.router, tags=["campaign"])
