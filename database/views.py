import datetime as dt
from typing import List, Optional, Tuple

from .models import AllThemes, Theme
from .status_code import StatusCode


def get_theme_by_secret(secret: str) -> Optional[Theme]:
    return AllThemes.get_or_none(AllThemes.secret == secret)


def get_theme_by_chat_user_id(chat_id: str, user_id: str) -> Optional[Theme]:
    return AllThemes.get_or_none(
        AllThemes.chat_id == chat_id, AllThemes.user_id == user_id
    )


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
    secret: str,
    message: str,
    user_id: str,
    username: str,
    chat_id: str,
    message_id: str,
) -> bool:
    theme = get_theme_by_secret(secret)
    if theme is None:
        return False
    Theme.create(
        theme=theme,
        message=message,
        user_id=user_id,
        username=username,
        chat_id=chat_id,
        message_id=message_id,
        timestamp=dt.datetime.now(),
    )
    return True


def get_messages(
    chat_id: str = None, user_id: str = None
) -> List[Tuple[str, str, str, str, str]]:
    theme = get_theme_by_chat_user_id(chat_id, user_id)
    if theme is None:
        return []
    messages = []
    for mes in Theme.select().where(Theme.theme == theme):
        messages.append(
            (
                mes.message,
                mes.user_id,
                mes.username,
                mes.chat_id,
                mes.message_id,
            )
        )
    return messages
