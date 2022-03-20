import logging

from pyrogram import Client, filters, types
from pyrogram.handlers import MessageHandler

from config import MAIN_BOT_API_HASH, MAIN_BOT_API_ID

from .bot_author import handler_author_list, handler_author_reply
from .bot_user import handler_user_text
from .command_add import filter_it_theme_chat, get_add_message
from .command_answer import filter_it_user_chat, get_answer_message
from .text_data import HELLO_MESSAGE
from .utils import delete_chat, user_is_bot

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


@app.on_message(filters.command('answer') & filters.private)  # type: ignore
async def handler_answer(client: Client, message: types.Message) -> None:
    await message.reply('Подождите, идет процесс создания чата')
    text_to_send = await get_answer_message(client, message, message.text)
    await message.reply(text_to_send)


@app.on_message(filters.text & filters.private)  # type: ignore
async def handler_text(_: Client, message: types.Message) -> None:
    if user_is_bot(message):
        return
    await message.reply(HELLO_MESSAGE)


@app.on_message(filters.left_chat_member)  # type: ignore
async def left_chat_member(client: Client, message: types.Message) -> None:
    logger.info('%s user leave', message.chat.id)
    if message.chat.members_count < 2:
        await delete_chat(client, message.chat.id)
        logger.info('Chat %s deleted', message.chat.id)
    await client.send_message(
        message.left_chat_member.id,
        f'Chat with theme {message.chat.title} deleted',
    )


app.add_handler(
    MessageHandler(
        handler_author_list,
        filters.group
        & filters.command('list')
        & filters.create(filter_it_theme_chat, 'theme_chat'),
    )
)
app.add_handler(
    MessageHandler(
        handler_author_reply,
        filters.group
        & filters.reply
        & filters.create(filter_it_theme_chat, 'theme_chat'),
    )
)

app.add_handler(
    MessageHandler(
        handler_user_text,
        filters.group & filters.create(filter_it_user_chat, 'user_chat'),
    )
)


app.run()
