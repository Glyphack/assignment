from datetime import datetime
from app.server.routes import api_router
from app.services.campaign.data_importer import CampaignDataFramesManager
from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
app = FastAPI(title="campaign_banner", version="0.1.0")

app.include_router(api_router)


@app.on_event("startup")
async def cache_csv_files_every_hour() -> None:
    print("started downloading csv files")
    await CampaignDataFramesManager.load_csv_files_to_memory()
    print("finished downloading csv files")


@app.on_event("startup")
@repeat_every(seconds=60)
async def cache_csv_files_every_hour() -> None:
    time = datetime.now()
    # only update csv files at the start of hour
    if not CampaignDataFramesManager.is_cache_valid():
        print("updating csv files")
        await CampaignDataFramesManager.load_csv_files_to_memory()
        print("finished updating csv files")
