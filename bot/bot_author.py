import logging

from pyrogram import Client, types

from .bot_author_utils import get_messages

logger = logging.getLogger(__name__)


async def handler_list(client: Client, message: types.Message) -> None:
    logger.info('handler_list')
    chat_id = message.chat.id
    user_id = message.from_user.id
    messages = await get_messages(str(chat_id), str(user_id), client)
    for msg_to_forward, text_to_send in messages:
        if msg_to_forward is not None:
            try:
                await msg_to_forward.forward(chat_id)
                continue
            except Exception:
                logger.exception('Error in forward')
        await message.reply(text_to_send)
    if len(messages) == 0:
        await message.reply('Нет сообщений')


async def handler_reply(
    client: Client, message: types.Message
) -> None:  # TODO
    logger.info('handler_reply')
