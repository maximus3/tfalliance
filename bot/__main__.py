import logging

from pyrogram import Client, filters, types

from config import MAIN_BOT_API_HASH, MAIN_BOT_API_ID

from .text_data import HELLO_MESSAGE
from .utils import delete_chat, get_add_message, user_is_bot

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
    text_to_send = await get_add_message(client, message, message.text)
    await message.reply(text_to_send)


@app.on_message(filters.text & filters.private)  # type: ignore
async def handler_text(_: Client, message: types.Message) -> None:
    if user_is_bot(message):
        return
    await message.reply(HELLO_MESSAGE)


@app.on_message(filters.left_chat_member)  # type: ignore
async def text(client: Client, message: types.Message) -> None:
    print(message)
    if message.chat.members_count < 2:
        delete_chat(client, message.chat.id)
        logger.info('Chat %s deleted', message.chat.id)
    with client:
        await client.send_message(
            message.left_chat_member.id,
            f'Chat with theme {message.chat.title} deleted',
        )


app.run()
