import time
from locust import HttpUser, task
import random


class GetCampaignUser(HttpUser):
    @task
    def get_random_campaign(self):
        self.client.get(f"/campaign/{random.randint(1,50)}")
