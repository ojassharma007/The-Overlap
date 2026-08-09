# config.py
from decouple import config

API_KEY = config('FOOTBALL_API_KEY')
BASE_URL = 'https://v3.football.api-sports.io'