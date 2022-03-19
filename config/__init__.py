import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
with open(BASE_DIR / 'config.json', encoding='utf-8') as f:
    data = json.load(f)


DATABASE_NAME = BASE_DIR / data['database_name']
MAIN_BOT_API_ID = data['main_bot_api_id']
MAIN_BOT_API_HASH = data['main_bot_api_hash']

BOT_FATHER_ID = '@BotFather'
BOT_FATHER_TEXTS = {
    'after_newbot': 'Alright, a new bot. How are we going to call it?'
    ' Please choose a name for your bot.',
    'after_name': "Good. Now let's choose a username for your bot. It must end in `bot`."
    ' Like this, for example: TetrisBot or tetris_bot.',
    'name_exists': 'Sorry, this username is already taken. Please try something different.',
    'done': 'Done!',
}
