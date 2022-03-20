import datetime as dt
from typing import List, Optional, Tuple

from .models import AllThemes, Messages, UserChat
from .status_code import StatusCode


def get_theme_by_secret(secret: str) -> Optional[Messages]:
    return AllThemes.get_or_none(AllThemes.secret == secret)


def get_theme_by_chat_user_id(
    chat_id: str, user_id: str
) -> Optional[AllThemes]:
    return AllThemes.get_or_none(
        AllThemes.chat_id == chat_id, AllThemes.user_id == user_id
    )


def get_user_chat_by_chat_id(chat_id: str) -> Optional[UserChat]:
    return UserChat.get_or_none(UserChat.chat_id == chat_id)


def get_user_chat_by_theme_user_id(
    theme: AllThemes, user_id: str
) -> Optional[UserChat]:
    return (
        UserChat.select()
        .where(UserChat.theme == theme, UserChat.user_id == user_id)
        .get_or_none()
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
        theme.delete_instance()
    return True


def get_theme_info(secret: str) -> Tuple[Optional[str], Optional[str]]:
    theme = get_theme_by_secret(secret)
    if theme is None:
        return None, None
    return theme.theme_name, theme.start_message


def get_msg_by_user_chat_text(user_chat: UserChat, text: str) -> Messages:
    return (
        Messages.select()
        .where(Messages.user_chat == user_chat, Messages.text == text)
        .get_or_none()
    )


def add_new_user_chat(
    secret: str, chat_id: str, user_id: str, username: str
) -> StatusCode:
    theme = get_theme_by_secret(secret)
    if theme is None:
        return StatusCode.THEME_NOT_EXISTS
    user_chat = get_user_chat_by_theme_user_id(theme, user_id)
    if user_chat is not None:
        return StatusCode.CHAT_ALREADY_EXISTS
    UserChat.create(
        theme=theme, chat_id=chat_id, user_id=user_id, username=username
    )
    return StatusCode.OK


def get_all_theme_chats() -> List[str]:
    result = []
    for theme in AllThemes.select():
        result.append(theme.chat_id)
    return result


def get_all_user_chats() -> List[str]:
    result = []
    for theme in UserChat.select():
        result.append(theme.chat_id)
    return result


def add_new_message(chat_id: str, text: str, message_id: str) -> StatusCode:
    user_chat = get_user_chat_by_chat_id(chat_id)
    if user_chat is None:
        return StatusCode.CHAT_NOT_EXISTS
    try:
        theme = user_chat.theme
    except Exception:
        return StatusCode.THEME_NOT_EXISTS
    Messages.create(
        theme=theme,
        user_chat=user_chat,
        text=text,
        message_id=message_id,
        timestamp=dt.datetime.now(),
    )
    return StatusCode.OK


def get_messages(
    chat_id: str, user_id: str
) -> List[Tuple[str, str, str, str, str]]:
    theme = get_theme_by_chat_user_id(chat_id, user_id)
    if theme is None:
        return []
    messages = []
    for mes in list(Messages.select().where(Messages.theme == theme)):
        messages.append(
            (
                mes.text,
                mes.user_chat.user_id,
                mes.user_chat.username,
                mes.user_chat.chat_id,
                mes.message_id,
            )
        )
    return messages


def get_chat_message_ids(
    author_chat_id: str, author_id: str, sender_id: str, text: str
) -> Tuple[Optional[str], Optional[str]]:
    theme = get_theme_by_chat_user_id(author_chat_id, author_id)
    if theme is None:
        return None, None
    user_chat = get_user_chat_by_theme_user_id(theme, sender_id)
    if user_chat is None:
        return None, None
    msg = get_msg_by_user_chat_text(user_chat, text)
    if msg is None:
        return user_chat.chat_id, None
    return user_chat.chat_id, msg.message_id
