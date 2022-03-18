from new_bot_registration import register_new_bot
from status_code import StatusCode

import database.views


def check_message_add(text):  # TODO
    splitted_text = text.split()
    if len(splitted_text) != 2:
        return StatusCode.WRONG_PARAMETERS_COUNT, None
    return StatusCode.OK, splitted_text[1]


def add_new_theme(theme_name, client):
    status, theme = database.views.add_new_theme(theme_name)
    if status:
        return StatusCode.ERROR_IN_ADD_TO_DATABASE, None
    status, bot_nick = register_new_bot(theme_name, client, theme)
    if status:
        return StatusCode.ERROR_IN_REGISTER_NEW_BOT, None
    return StatusCode.OK, bot_nick
