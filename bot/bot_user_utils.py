import logging

from pyrogram import types

import database.views

logger = logging.getLogger(__name__)


async def save_message(message: types.Message, text: str) -> str:
    chat_id = message.chat.id
    status_db_add = database.views.add_new_message(
        str(chat_id), text, str(message.message_id)
    )
    if status_db_add:
        logger.error('Message by chat_id=%s error: %s', chat_id, status_db_add)
        return 'Error add_new_message'
    logger.info('Message by chat_id=%s saved', chat_id)
    return '__Сообщение отправлено__'  # TODO
