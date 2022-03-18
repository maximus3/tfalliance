import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
with open(BASE_DIR / 'config.json', encoding='utf-8') as f:
    data = json.load(f)


DATABASE_NAME = data['database_name']
