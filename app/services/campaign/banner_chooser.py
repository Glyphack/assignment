from collections import Counter
import pandas as pd
from app.services.campaign.constants import CampaignBannersDataFields


class BannerChooser:
    def __init__(self, campaign_banners: pd.DataFrame) -> None:
        super().__init__()
        self._campaign_all_banners = campaign_banners
        self._campaign_banners_with_click = campaign_banners[campaign_banners[
            CampaignBannersDataFields.CLICKED_ID_KEY].notna()]
        self._campaign_banners_with_conversion = campaign_banners[
            campaign_banners[CampaignBannersDataFields.CONVERSION_ID_KEY
                             ].notna()]

    def choose_banners(self):
        return self.what_to_show_for_campaign()

    def what_to_show_for_campaign(self):
        """
        return list of what should be served for the campaign based on banners with conversion
        """
        number_of_banners_with_conversion = len(
            self._campaign_banners_with_conversion
        )
        if number_of_banners_with_conversion >= 10:
            return self._get_top_banners_id_based_on_revenue(count=10)

        if number_of_banners_with_conversion in range(5, 10):
            return self._get_top_banners_id_based_on_revenue(
                count=number_of_banners_with_conversion
            )

        if number_of_banners_with_conversion in range(1, 5):
            banners = self._get_top_banners_id_based_on_revenue()
            banners += self._get_top_banners_based_on_click(
                count=5 - number_of_banners_with_conversion
            )
            return banners

        banners = self._get_top_banners_based_on_click(count=5)
        if len(banners) < 5:
            banners += self._get_random_banners(count=5 - len(banners))
        return banners

    def _get_top_banners_id_based_on_revenue(self, count: int = None):
        if count is None:
            count = len(self._campaign_banners_with_conversion)
        top_banners = self._campaign_banners_with_conversion.nlargest(
            count, columns=[CampaignBannersDataFields.REVENUE_KEY], keep="all"
        )
        return top_banners[CampaignBannersDataFields.BANNER_ID_KEY].to_list()

    def _get_top_banners_based_on_click(self, count: int = None):
        if count is None:
            count = len(self._campaign_banners_with_click)
        clicked_banners = self._campaign_banners_with_click[
            CampaignBannersDataFields.BANNER_ID_KEY].to_list()

        most_clicked_banners = Counter(clicked_banners).most_common(count)
        return [banner_id for banner_id, _ in most_clicked_banners]

    def _get_random_banners(self, count: int = None):
        if count is None:
            count = len(self._campaign_all_banners)
        return self._campaign_all_banners.sample(count)
