import logging
from datetime import datetime, timedelta

from app.core import config
from app.utils.read_csv import get_csv_async

logger = logging.getLogger(__name__)


class CampaignDataFramesManager:
    cache = {}
    updated_time = datetime.now()
    ttl_hours = config.CAMPAIGN_CSV_CACHE_TTL_HOURS

    @classmethod
    async def get_data_frame(cls, sheet_name, index):
        cached_data = cls.cache.get(cls.get_cache_key(sheet_name, index))
        if cached_data is not None:
            return cached_data

        csv = await cls.download_campaign_data_csv(sheet_name, index)
        return csv

    @classmethod
    async def load_csv_files_to_memory(cls):
        for index in range(1, 5):
            for sheet_name in ["conversions", "impressions", "clicks"]:
                csv = await cls.download_campaign_data_csv(
                    sheet_name=sheet_name, index=index
                )
                if cls.should_replace_csv(
                    new=csv,
                    previous=cls.cache.get(
                        cls.get_cache_key(sheet_name, index)
                    )
                ):
                    cls.set_cache(cls.get_cache_key(sheet_name, index), csv)
        cls.updated_time = datetime.now()

    @classmethod
    def is_cache_valid(cls):
        """
        we should update cache every hour
        """
        return cls.updated_time + timedelta(hours=cls.ttl_hours
                                            ) > datetime.now()

    @staticmethod
    def get_cache_key(sheet_name, index):
        return sheet_name + str(index)

    @classmethod
    def set_cache(cls, key, value):
        cls.cache[key] = value

    @staticmethod
    async def download_campaign_data_csv(sheet_name, index):
        url = f'{config.STATIC_CONTENT_BASE_URL}/csv/{index}/{sheet_name}_{index}.csv'
        csv = await get_csv_async(url)
        return csv

    @classmethod
    def should_replace_csv(cls, new, previous):
        if previous is None:
            return True
        duplicate_percentage = cls.get_csv_duplicate_percentage(new, previous)
        if duplicate_percentage > config.CSV_DUPLICATE_PERCENTAGE_REJECT_THRESHOLD:
            logger.warning(
                "duplicate csv rejected",
                extra={
                    "first_csv_updated_at": cls.updated_time,
                    "second_csv_updated_at": datetime.now()
                }
            )
            return False
        return True

    @staticmethod
    def get_csv_duplicate_percentage(first, second):
        duplicate_rows = first.merge(second, how='inner', indicator=False)
        return len(duplicate_rows) / len(second) * 100
