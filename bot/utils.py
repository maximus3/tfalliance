import logging
import random
import string
from typing import Tuple

from pyrogram import Client, types

import database.views

from .status_code import StatusCode

logger = logging.getLogger(__name__)


async def create_new_chat(
    client: Client, theme_name: str, user_id: str, start_message: str
) -> Tuple[StatusCode, str, str]:  # TODO
    with client:
        chat = await client.create_group(theme_name, user_id)
        await client.send_message(chat.id, start_message)
        invite_link = await client.create_chat_invite_link(
            chat.id, member_limit=1
        )
    return StatusCode.OK, str(chat.id), invite_link.invite_link


def check_message_add(
    text: str,
) -> Tuple[StatusCode, str, str]:  # TODO: validate
    split_text = text.split('\n')
    if len(split_text) < 2:
        return StatusCode.WRONG_PARAMETERS_COUNT, '', ''
    com_and_theme = split_text[0].split()
    start_message = '\n'.join(split_text[1:])
    if len(com_and_theme) < 2:
        return StatusCode.WRONG_PARAMETERS_COUNT, '', ''
    _, theme = com_and_theme[:1], ' '.join(com_and_theme[1:])
    return StatusCode.OK, theme, start_message


async def add_new_theme(
    theme_name: str, start_message: str, client: Client, user_id: str
) -> Tuple[StatusCode, str]:

    status_create, chat_id, invite_link = await create_new_chat(
        client, theme_name, user_id, start_message
    )
    if status_create:
        logger.error('Chat by theme=%s error: %s', theme_name, status_create)
        return StatusCode.ERROR_IN_REGISTER_NEW_BOT, ''
    logger.info(
        'Chat by theme=%s created with chat_id=%s', theme_name, chat_id
    )

    status_db_add = database.views.add_new_theme(
        theme_name, user_id, chat_id, start_message
    )
    if status_db_add:
        logger.error('Chat by theme=%s error: %s', theme_name, status_db_add)
        return StatusCode.ERROR_IN_ADD_TO_DATABASE, ''
    logger.info('Chat by theme=%s db created', theme_name)

    return StatusCode.OK, invite_link


async def get_add_message(
    client: Client, message: types.Message, text: str
) -> str:
    status, theme_name, start_text = check_message_add(text)
    user_id = get_user_id(message)
    if status:
        logger.error('check_message_add error: %s', status)
        return 'Error'  # TODO
    status, invite_link = await add_new_theme(
        theme_name, start_text, client, user_id
    )
    if status:
        logger.error('add_new_theme error: %s', status)
        if status == StatusCode.ERROR_THEME_ALREADY_EXISTS:
            return 'Такая тема уже есть'
        return 'Error'  # TODO
    return f'{invite_link}'  # TODO


def get_username(message: types.Message) -> str:
    return message.from_user.username


def get_user_id(message: types.Message) -> str:
    return str(message.from_user.id)


def user_is_bot(message: types.Message) -> bool:
    return message.from_user.is_bot


def random_word(length: int) -> str:
    return ''.join(
        random.choice(string.ascii_lowercase) for _ in range(length)
    )


def delete_chat(client: Client, chat_id: int) -> bool:
    with client:
        client.leave_chat(chat_id, True)
        return database.views.delete_theme_by_chat(chat_id)
