import logging

from pyrogram import Client, types

from .bot_user_utils import save_message

logger = logging.getLogger(__name__)


async def handler_user_text(_: Client, message: types.Message) -> None:
    logger.info('handler_user_text')
    text_to_send = await save_message(message, message.text)
    await message.reply(text_to_send)
