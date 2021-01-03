from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/campaign/{campaign_id}", response_class=HTMLResponse)
async def get_campaign_banners(request: Request, campaign_id):
    return "hello" + campaign_id
