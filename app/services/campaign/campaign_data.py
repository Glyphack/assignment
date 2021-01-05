import pandas as pd
from app.services.campaign.constants import CampaignBannersDataFields
from app.services.campaign import data_importer


async def get_campaign_all_banners_data_frame(campaign_id: int, index: int):
    conversions = await data_importer.CampaignDataFramesManager.get_data_frame(
        "conversions", index
    )
    clicks = await data_importer.CampaignDataFramesManager.get_data_frame(
        "clicks", index
    )
    impressions = await data_importer.CampaignDataFramesManager.get_data_frame(
        "impressions", index
    )

    merged_conversion_clicks = pd.merge(
        conversions, clicks, how="right", on="click_id", validate="one_to_one"
    )
    merged_all = pd.merge(
        merged_conversion_clicks,
        impressions,
        how="outer",
        on=[
            CampaignBannersDataFields.CAMPAIGN_ID_KEY,
            CampaignBannersDataFields.BANNER_ID_KEY
        ]
    )

    # we don't want to show a banner twice so we remove duplicate rows that might be in dataframes
    merged = merged_all.drop_duplicates(
        subset=[
            CampaignBannersDataFields.CAMPAIGN_ID_KEY,
            CampaignBannersDataFields.BANNER_ID_KEY
        ]
    )
    return merged.query(
        f"{CampaignBannersDataFields.CAMPAIGN_ID_KEY} == {campaign_id}"
    )
