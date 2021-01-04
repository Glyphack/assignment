from app.tests.utils import lists_are_equal
import numpy as np
import pandas as pd
from app.services.campaign import banner_chooser
from app.services.campaign.constants import CampaignBannersDataFields


def test_banner_chooser():
    test_cases = [
        # Case 1: all banners have conversion
        {
            'input':
                [
                    [1, 1, 1, 1, 1], [2, 1, 2, 2, 5], [3, 1, 3, 3, 3],
                    [4, 1, 4, 4, 8], [5, 1, 5, 5, 4], [6, 1, 6, 6, 5],
                    [7, 1, 7, 7, 10], [8, 1, 8, 8, 11], [9, 1, 9, 9, 13],
                    [10, 1, 10, 10, 9]
                ],
            'expected': [9, 8, 7, 10, 4, 2, 6, 5, 3, 1],
        },
        # Case 2: not enough banners with convension
        {
            'input':
                [
                    [1, 1, 1, np.nan, np.nan], [1, 1, 2, np.nan, np.nan],
                    [3, 1, 3, np.nan, np.nan], [4, 1, 4, np.nan, np.nan],
                    [4, 1, 5, np.nan, np.nan], [4, 1, 6, np.nan, np.nan],
                    [7, 1, 7, np.nan, np.nan], [8, 1, 8, 8, 11],
                    [9, 1, 9, 9, 13], [10, 1, 10, 10, 9]
                ],
            'expected': [9, 8, 10, 4, 1],
        },
        # Case 3: no banners with conversion
        {
            'input':
                [
                    [1, 1, 1, np.nan, np.nan], [1, 1, 2, np.nan, np.nan],
                    [3, 1, 3, np.nan, np.nan], [4, 1, 4, np.nan, np.nan],
                    [4, 1, 5, np.nan, np.nan], [4, 1, 6, np.nan, np.nan],
                    [7, 1, 7, np.nan, np.nan], [8, 1, 8, np.nan, np.nan],
                    [9, 1, 9, np.nan, np.nan], [10, 1, 10, np.nan, np.nan]
                ],
            'expected': [4, 1, 3, 7, 8],
        },
    ]
    for test_case in test_cases:
        campaign_banners_data_frame = pd.DataFrame(
            test_case["input"],
            columns=[
                CampaignBannersDataFields.BANNER_ID_KEY,
                CampaignBannersDataFields.CAMPAIGN_ID_KEY,
                CampaignBannersDataFields.CLICKED_ID_KEY,
                CampaignBannersDataFields.CONVERSION_ID_KEY,
                CampaignBannersDataFields.REVENUE_KEY
            ]
        )
        chosen_banners = banner_chooser.BannerChooser(
            campaign_banners_data_frame
        ).choose_banners()
        assert lists_are_equal(chosen_banners, test_case["expected"])
