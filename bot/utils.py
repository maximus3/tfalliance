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
) -> Tuple[StatusCode, str, str]:
    chat = await client.create_group(theme_name, user_id)
    await client.send_message(chat.id, start_message)
    invite_link = await client.create_chat_invite_link(chat.id, member_limit=1)
    return StatusCode.OK, str(chat.id), invite_link.invite_link


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


async def delete_chat(client: Client, chat_id: int) -> bool:
    await client.leave_chat(chat_id, True)
    return database.views.delete_theme_by_chat(chat_id)
