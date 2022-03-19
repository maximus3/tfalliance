import logging
import random
import string
from time import sleep
from typing import Tuple

from pyrogram import Client, types

from config import BOT_FATHER_ID, BOT_FATHER_TEXTS

from .status_code import StatusCode

loggger = logging.getLogger(__name__)

time_to_sleep = 5


def random_word(length: int) -> str:
    return ''.join(
        random.choice(string.ascii_lowercase) for i in range(length)
    )


def get_token(text: str) -> str:
    return text.splitlines()[3]


async def get_message_from_bot_father(client: Client) -> types.Message:
    message_info = await client.get_history(chat_id=BOT_FATHER_ID, limit=1)
    return message_info[0]


async def register_new_bot(
    theme_name: str, client: Client
) -> Tuple[StatusCode, str, str]:  # TODO: make work pool, many msg in one time
    with client:
        await client.send_message(BOT_FATHER_ID, '/newbot')
        sleep(time_to_sleep)
        message = await get_message_from_bot_father(client)
        if message.text != BOT_FATHER_TEXTS['after_newbot']:
            loggger.error('After /newbot text: %s', message.text)
            return StatusCode.ERROR_IN_REGISTER_NEW_BOT, '', ''
        loggger.info('After /newbot OK')

        await client.send_message(BOT_FATHER_ID, theme_name)
        sleep(time_to_sleep)
        message = await get_message_from_bot_father(client)
        if message.text != BOT_FATHER_TEXTS['after_name']:
            loggger.error('After name text: %s', message.text)
            return StatusCode.ERROR_IN_REGISTER_NEW_BOT, '', ''
        loggger.info('After name OK')

        done = False
        while not done:
            bot_name = f'memas_alliance_{random_word(8)}_bot'
            await client.send_message(BOT_FATHER_ID, bot_name)
            sleep(time_to_sleep)
            message = await get_message_from_bot_father(client)
            if message.text == BOT_FATHER_TEXTS['name_exists']:
                loggger.error('After bot nick ALREADY EXISTS')
                continue
            if not message.text.startswith(BOT_FATHER_TEXTS['done']):
                loggger.error('After bot nick text: %s', message.text)
                return StatusCode.ERROR_IN_REGISTER_NEW_BOT, '', ''
            loggger.info('After bot nick OK')
            token = get_token(message.text)
            break

    return StatusCode.OK, token, bot_name
