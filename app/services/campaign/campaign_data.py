import pandas as pd
from app.services.campaign.constants import CampaignBannersDataFields
from app.services.static_files import csv_reader


def get_campaign_all_banners_data_frame(campaign_id: int, index: int):
    conversions = csv_reader.get_conversions_data_frame(index=index)
    clicks = csv_reader.get_clicks_data_frame(index=index)
    impressions = csv_reader.get_impressions_data_frame(index=index)

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
