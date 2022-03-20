import logging
from typing import Tuple

from pyrogram import Client, filters, types

import database.views

from .status_code import StatusCode
from .utils import create_new_chat, get_user_id, get_username

logger = logging.getLogger(__name__)


def check_message_answer(
    text: str,
) -> Tuple[StatusCode, str]:
    split_text = text.split()
    if len(split_text) != 2:
        return StatusCode.WRONG_PARAMETERS_COUNT, ''
    secret = split_text[1]
    return StatusCode.OK, secret


async def add_new_answer(
    secret: str, client: Client, user_id: str, username: str
) -> Tuple[StatusCode, str]:
    theme_name, start_message = database.views.get_theme_info(secret)
    if theme_name is None or start_message is None:
        return StatusCode.ERROR_WRONG_CODE, ''
    status_create, chat_id, invite_link = await create_new_chat(
        client, theme_name, user_id, start_message
    )
    if status_create:
        logger.error(
            'Chat by theme=%s error: %s by user=%s',
            theme_name,
            status_create,
            user_id,
        )
        return StatusCode.ERROR_IN_REGISTER_NEW_BOT, ''
    logger.info(
        'Chat by theme=%s created with chat_id=%s by user=%s',
        theme_name,
        chat_id,
        user_id,
    )

    status_db_add = database.views.add_new_user_chat(
        secret, chat_id, user_id, username
    )
    if status_db_add:
        logger.error(
            'Chat by theme=%s error: %s by user=%s',
            theme_name,
            status_db_add,
            user_id,
        )
        return StatusCode.ERROR_IN_ADD_TO_DATABASE, ''
    logger.info('Chat by theme=%s db created by user=%s', theme_name, user_id)

    return StatusCode.OK, invite_link


async def get_answer_message(
    client: Client, message: types.Message, text: str
) -> str:
    status, secret = check_message_answer(text)
    user_id = get_user_id(message)
    username = get_username(message)
    if status:
        logger.error(
            'check_message_answer error: %s by user=%s', status, user_id
        )
        return 'Error check_message_answer'  # TODO
    status, invite_link = await add_new_answer(
        secret, client, user_id, username
    )
    if status:
        logger.error('add_new_answer error: %s by user=%s', status, user_id)
        if status == StatusCode.ERROR_WRONG_CODE:
            return 'Неправильный код'
        return 'Error add_new_answer'  # TODO

    return f'{invite_link}'  # TODO


def filter_it_user_chat(
    _: filters.Filter, __: Client, update: types.Message
) -> bool:
    chats = database.views.get_all_user_chats()
    logger.info(
        'filter_it_user_chat message from chat_id=%s, all_chats=%s, %s',
        str(update.chat.id),
        str(chats),
        str(str(update.chat.id) in chats),
    )
    return str(update.chat.id) in chats
