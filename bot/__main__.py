from pyrogram import Client, filters

from config import MAIN_BOT_API_HASH, MAIN_BOT_API_ID

api_id = MAIN_BOT_API_ID
api_hash = MAIN_BOT_API_HASH
app = Client('main_bot', api_id, api_hash)


@app.on_message(filters.command('start') & filters.private)
async def handler_start(client, message):
    await message.reply(
        """Привет!
Напиши /list для просмотра всех существующих тем
Напиши /add для добавления новой темы"""
    )


@app.on_message(filters.command('list') & filters.private)
async def handler_list(client, message):
    await message.reply("""/list""")


@app.on_message(filters.command('add') & filters.private)
async def handler_add(client, message):
    await message.reply("""/add""")


@app.on_message(filters.command('reg') & filters.private)
async def handler_reg(client, message):
    await message.reply("""/reg""")


@app.on_message(filters.text & filters.private)
async def handler_text(client, message):
    await message.reply(
        """Привет!
Напиши `/list` для просмотра всех существующих тем
Напиши `/add` для добавления новой темы"""
    )


app.run()
