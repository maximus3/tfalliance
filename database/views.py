import datetime as dt
from typing import List, Optional, Tuple

from .models import AllThemes, Theme
from .status_code import StatusCode


def get_theme_by_secret(secret: str) -> Optional[Theme]:
    return AllThemes.get_or_None(AllThemes.secret == secret)


def add_new_theme(
    theme_name: str,
    user_id: str,
    chat_id: str,
    start_message: str,
    secret: str,
) -> StatusCode:
    AllThemes.create(
        theme_name=theme_name,
        start_message=start_message,
        chat_id=chat_id,
        user_id=user_id,
        secret=secret,
    )
    return StatusCode.OK


def delete_theme_by_chat(chat_id: int) -> bool:
    theme = (
        AllThemes.select().where(AllThemes.chat_id == chat_id).get_or_none()
    )
    if theme:
        theme.delete()
    return True


def add_message(
    secret: str, message: str, user_id: str, chat_id: str, message_id: str
) -> bool:
    theme = get_theme_by_secret(secret)
    if theme is None:
        return False
    Theme.create(
        theme=theme,
        message=message,
        user_id=user_id,
        chat_id=chat_id,
        message_id=message_id,
        timestamp=dt.datetime.now(),
    )
    return True


def get_messages(secret) -> List[Tuple[str, str, str, str]]:
    """

    :param secret: secret topic's code
    :return: List of Tuple of message, user_id, chat_id, message_id
    """
    theme = get_theme_by_secret(secret)
    if theme is None:
        return []
    messages = []
    for mes in Theme.select().where(Theme.theme == theme):
        messages.append(
            (mes.message, mes.user_id, mes.chat_id, mes.message_id)
        )
    return messages
