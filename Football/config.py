# config.py
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('FOOTBALL_API_KEY')
BASE_URL = 'https://v3.football.api-sports.io'

