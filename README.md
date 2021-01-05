# Application
This application serves banners for campaign based on banner performance and business rules.

## How it works
this application contains a endpoint `campaigns/{campaign_id}`, which shows banners for campaign_id.
It downloads csv from s3 on startup and try to update csv data every 12 hour.

## load testing
load testing is done using locust. see `scripts/locustfile.py`

## url
http://shayeganassignemnt-env-1.eba-qd2hf6xr.eu-west-1.elasticbeanstalk.com/campaign/1
