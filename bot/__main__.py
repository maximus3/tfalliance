import logging

from pyrogram import Client, filters, types

from config import BOT_FATHER_ID, MAIN_BOT_API_HASH, MAIN_BOT_API_ID

from .utils import (
    get_add_message,
    user_is_bot
)

from .text_data import HELLO_MESSAGE

api_id = MAIN_BOT_API_ID
api_hash = MAIN_BOT_API_HASH
app = Client('main_bot', api_id, api_hash)
logger = logging.getLogger(__name__)


@app.on_message(filters.command('start') & filters.private)  # type: ignore
async def handler_start(_: Client, message: types.Message) -> None:
    await message.reply(HELLO_MESSAGE)


@app.on_message(filters.command('add') & filters.private)  # type: ignore
async def handler_add(client: Client, message: types.Message) -> None:
    await message.reply('Подождите, идет процесс создания чата')
    text_to_send = await get_add_message(client, message.text)
    await message.reply(text_to_send)


@app.on_message(filters.text & filters.private)  # type: ignore
async def handler_text(_: Client, message: types.Message) -> None:
    if user_is_bot(message):
        return
    await message.reply(HELLO_MESSAGE)


# @app.on_message(filters.group_chat_created)
# async def text(client, message):
#     theme_name = message.chat.title
#     await message.reply(f'''Тема {theme_name} создана
# Пришлите начальное сообщение для темы''')


app.run()
