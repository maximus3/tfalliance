from typing import Tuple
from pyrogram import Client

from .status_code import StatusCode


def register_new_bot(
    theme_name: str, client: Client
) -> Tuple[StatusCode, str, str]:  # TODO
    print(theme_name, client)
    return StatusCode.ERROR_IN_REGISTER_NEW_BOT, '', ''
