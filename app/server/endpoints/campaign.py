import random

from app.services.campaign.banner_chooser import BannerChooser
from app.services.campaign.campaign_data import (
    get_campaign_all_banners_data_frame,
)
from app.services.static_files import banner_image
from app.services.templates.template import render_to_string
from app.utils.time import get_hour_quarter
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/campaign/{campaign_id}", response_class=HTMLResponse)
async def get_campaign_banners(request: Request, campaign_id):
    all_banners = await get_campaign_all_banners_data_frame(
        campaign_id, get_hour_quarter()
    )
    if all_banners.empty:
        raise HTTPException(status_code=404, detail="campaign not found")
    banner_chooser = BannerChooser(all_banners)
    banners = banner_chooser.choose_banners()
    banner_images = [
        banner_image.get_banner_image_url(banner) for banner in banners
    ]
    random.shuffle(banners)
    return render_to_string('campaign.html', banners=banner_images)
