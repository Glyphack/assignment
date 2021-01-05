import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))

CSV_FILES_PATH = os.path.join(os.path.dirname(BASEDIR), '/static/csv')

STATIC_CONTENT_BASE_URL = os.getenv("STATIC_CONTENT_URL")
