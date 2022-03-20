import logging

import pyrogram.errors
from pyrogram import Client, types

from .bot_author_utils import get_messages, reply_message

logger = logging.getLogger(__name__)


async def handler_author_list(client: Client, message: types.Message) -> None:
    logger.info('handler_list')
    chat_id = message.chat.id
    user_id = message.from_user.id
    messages = await get_messages(str(chat_id), str(user_id))
    if len(messages) != 0:
        await message.reply(f'__Всего сообщений:__ **{len(messages)}**')
    for msg_to_forward_data, text_to_send in messages:
        try:
            await client.forward_messages(
                chat_id,
                from_chat_id=msg_to_forward_data[0],
                message_ids=msg_to_forward_data[1],
            )
            continue
        except pyrogram.errors.exceptions.bad_request_400.MessageIdInvalid:
            logger.exception('Error in forward')
        await message.reply(text_to_send)
    if len(messages) == 0:
        await message.reply('__Нет сообщений__')


async def handler_author_reply(client: Client, message: types.Message) -> None:
    logger.info('handler_reply')
    if await reply_message(client, message):
        await message.reply('__Сообщение отправлено__')
    else:
        await message.reply('**Произошла ошибка**')
