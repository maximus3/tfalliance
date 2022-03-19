import logging

from pyrogram import Client, filters, types

from config import BOT_FATHER_ID, MAIN_BOT_API_HASH, MAIN_BOT_API_ID

from .utils import (
    get_add_message,
    get_list_message,
    get_reg_message,
    get_username,
)

api_id = MAIN_BOT_API_ID
api_hash = MAIN_BOT_API_HASH
app = Client('main_bot', api_id, api_hash)
logger = logging.getLogger(__name__)


@app.on_message(filters.command('start') & filters.private)  # type: ignore
async def handler_start(_: Client, message: types.Message) -> None:
    await message.reply(
        """Привет!
Напиши `/list` для просмотра всех существующих тем
Напиши `/add` для добавления новой темы"""
    )


@app.on_message(filters.command('list') & filters.private)  # type: ignore
async def handler_list(_: Client, message: types.Message) -> None:
    text_to_send = get_list_message()
    await message.reply(text_to_send)


@app.on_message(filters.command('add') & filters.private)  # type: ignore
async def handler_add(client: Client, message: types.Message) -> None:
    await message.reply('Подождите, идет процесс создания бота')
    text_to_send = await get_add_message(client, message.text)
    await message.reply(text_to_send)


@app.on_message(filters.command('reg') & filters.private)  # type: ignore
async def handler_reg(_: Client, message: types.Message) -> None:
    text_to_send = get_reg_message(message.text, message)
    await message.reply(text_to_send)


@app.on_message(filters.text & filters.private)  # type: ignore
async def handler_text(_: Client, message: types.Message) -> None:
    username = get_username(message)
    if '@' + username == BOT_FATHER_ID:
        return
    await message.reply(
        """Привет!
Напиши `/list` для просмотра всех существующих тем
Напиши `/add` для добавления новой темы"""
    )


app.run()
