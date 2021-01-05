import pandas as pd
import io
import aiohttp


async def get_csv_async(url):
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            if response.status_code != 200:
                return None
            with io.StringIO(await response.text()) as text_io:
                return pd.read_csv(text_io)
