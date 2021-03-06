import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
with open(BASE_DIR / 'config.json', encoding='utf-8') as f:
    data = json.load(f)


DATABASE_NAME = BASE_DIR / data['database_name']
MAIN_BOT_API_ID = data['main_bot_api_id']
MAIN_BOT_API_HASH = data['main_bot_api_hash']
