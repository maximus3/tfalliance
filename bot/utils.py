import logging
from typing import Tuple

from pyrogram import Client, types

import database.views
from config import SECRET_KEY

from .new_bot_registration import register_new_bot
from .status_code import StatusCode

logger = logging.getLogger(__name__)


def start_new_chat(tg_bot_token: str) -> StatusCode:  # TODO
    logger.info('Start new bot with token=%s', tg_bot_token)
    return StatusCode.OK


def check_message_add(text: str) -> Tuple[StatusCode, str]:  # TODO: validate
    splitted_text = text.split()
    if len(splitted_text) < 2:
        return StatusCode.WRONG_PARAMETERS_COUNT, ''
    return StatusCode.OK, ' '.join(splitted_text[1:])


async def add_new_theme(
    theme_name: str, client: Client
) -> Tuple[StatusCode, str]:
    status_check_db_add = database.views.check_new_theme(theme_name)
    if status_check_db_add:
        logger.error(
            'Bot by theme=%s error: %s', theme_name, status_check_db_add
        )
        return StatusCode.ERROR_THEME_ALREADY_EXISTS, ''

    status_register, tg_bot_token, bot_nick = await register_new_bot(
        theme_name, client
    )
    if status_register:
        logger.error('Bot by theme=%s error: %s', theme_name, status_register)
        return StatusCode.ERROR_IN_REGISTER_NEW_BOT, ''
    logger.info(
        'Bot by theme=%s created with username=%s', theme_name, bot_nick
    )

    status_db_add = database.views.add_new_theme(
        theme_name, tg_bot_token, bot_nick
    )
    if status_db_add:
        logger.error('Bot by theme=%s error: %s', theme_name, status_db_add)
        return StatusCode.ERROR_IN_ADD_TO_DATABASE, ''
    logger.info('Bot by theme=%s db created', theme_name)

    status_run_bot = start_new_chat(tg_bot_token)
    if status_run_bot:
        logger.error(
            'Bot by theme=%s start error: %s', theme_name, status_run_bot
        )
        return StatusCode.RUN_BOT_ERROR, ''
    logger.info('Bot by theme=%s run', theme_name)

    return StatusCode.OK, bot_nick


def get_list_message() -> str:
    text = 'Список всех тем:\n'
    themes_list = database.views.get_themes_list()
    for theme_name, bot_nick in themes_list:
        text += f'{theme_name}\t@{bot_nick}\n'
    return text


async def get_add_message(client: Client, text: str) -> str:
    status, theme_name = check_message_add(text)
    if status:
        logger.error('check_message_add error: %s', status)
        return 'Error'  # TODO
    status, bot_nick = await add_new_theme(theme_name, client)
    if status:
        logger.error('add_new_theme error: %s', status)
        if status == StatusCode.ERROR_THEME_ALREADY_EXISTS:
            return 'Такая тема уже есть'
        return 'Error'  # TODO
    return f'@{bot_nick}'  # TODO


def get_username(message: types.Message) -> str:
    return message.from_user.username


def get_user_id(message: types.Message) -> str:
    return str(message.from_user.id)


def get_reg_message(text: str, message: types.Message) -> str:
    splitted_text = text.split()
    if len(splitted_text) != 2:
        return 'Error format'  # TODO
    user_tg_id, username = get_user_id(message), get_username(message)
    if splitted_text[1] == SECRET_KEY:
        logger.info('Add admin %s %s', user_tg_id, username)
        if database.views.add_admin(user_tg_id, username):
            return 'Ok'  # TODO
        return 'Error db'  # TODO

    logger.info('%s wrong code', user_tg_id)
    return 'Error code'
