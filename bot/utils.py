from typing import Tuple

from pyrogram import Client

import database.views

from .new_bot_registration import register_new_bot
from .status_code import StatusCode


def check_message_add(text: str) -> Tuple[StatusCode, str]:  # TODO
    splitted_text = text.split()
    if len(splitted_text) != 2:
        return StatusCode.WRONG_PARAMETERS_COUNT, ''
    return StatusCode.OK, splitted_text[1]


def add_new_theme(theme_name: str, client: Client) -> Tuple[StatusCode, str]:
    status_register, tg_bot_token, bot_nick = register_new_bot(
        theme_name, client
    )
    if status_register:
        return StatusCode.ERROR_IN_REGISTER_NEW_BOT, ''
    status_db_add = database.views.add_new_theme(
        theme_name, tg_bot_token, bot_nick
    )
    if status_db_add:
        return StatusCode.ERROR_IN_ADD_TO_DATABASE, ''
    return StatusCode.OK, bot_nick
