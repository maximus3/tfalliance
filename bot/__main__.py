import logging

import utils
from pyrogram import Client, filters

from config import MAIN_BOT_API_HASH, MAIN_BOT_API_ID

api_id = MAIN_BOT_API_ID
api_hash = MAIN_BOT_API_HASH
app = Client('main_bot', api_id, api_hash)
logger = logging.getLogger(__name__)


@app.on_message(filters.command('start') & filters.private)
async def handler_start(client, message):
    logger.info(client, message)
    await message.reply(
        """Привет!
Напиши /list для просмотра всех существующих тем
Напиши /add для добавления новой темы"""
    )


@app.on_message(filters.command('list') & filters.private)
async def handler_list(client, message):
    logger.info(client, message)
    print(client, message)
    await message.reply("""/list""")


@app.on_message(filters.command('add') & filters.private)
async def handler_add(client, message):
    logger.info(client, message)
    status, theme_name = utils.check_message_add(message.text)
    if status:
        await message.reply("""Error""")  # TODO
        return
    status, bot_nick = utils.add_new_theme(theme_name, client)
    if status:
        await message.reply("""Error""")  # TODO
        return
    await message.reply(f'{bot_nick}')  # TODO


@app.on_message(filters.command('reg') & filters.private)
async def handler_reg(client, message):
    logger.info(client, message)
    await message.reply("""/reg""")


@app.on_message(filters.text & filters.private)
async def handler_text(client, message):
    logger.info(client, message)
    await message.reply(
        """Привет!
Напиши `/list` для просмотра всех существующих тем
Напиши `/add` для добавления новой темы"""
    )


app.run()
