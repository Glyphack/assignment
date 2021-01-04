from datetime import datetime
from app.core import config
from app.utils.read_csv import get_csv_async


class CampaignDataFramesManager:
    cache = {}
    updated_time = datetime.now()

    @classmethod
    async def get_data_frame(cls, sheet_name, index):
        cached_data = cls.cache.get(cls.get_cache_key(sheet_name, index))
        if cached_data is not None and cls.is_cache_valid():
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
                cls.set_cache(cls.get_cache_key(sheet_name, index), csv)
        cls.updated_time = datetime.now()

    @classmethod
    def is_cache_valid(cls):
        """
        we should update cache every hour
        """
        return cls.updated_time.hour == datetime.now().hour

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
