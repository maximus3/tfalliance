from typing import List, Tuple

import peewee

from .models import AllThemes, User
from .status_code import StatusCode


def add_new_theme(
    theme_name: str, tg_bot_token: str, bot_nick: str
) -> StatusCode:
    if (
        AllThemes.select().where(AllThemes.theme_name == theme_name).count()
        > 0
    ):
        return StatusCode.THEME_ALREADY_EXISTS
    try:
        AllThemes.create(
            theme_name=theme_name, tg_bot_token=tg_bot_token, bot_nick=bot_nick
        )
    except peewee.IntegrityError as exc:
        if str(exc).startswith('UNIQUE'):
            return StatusCode.THEME_ALREADY_EXISTS
        return StatusCode.ERROR_IN_ADD_TO_DATABASE
    return StatusCode.OK


def get_themes_list() -> List[Tuple[str, str]]:
    result = []
    for theme in AllThemes.select():
        result.append((theme.theme_name, theme.bot_nick))
    return result


def add_admin(user_tg_id: str, username: str) -> bool:
    if User.select().where(User.user_tg_id == user_tg_id).count() > 0:
        user = User.select().where(User.user_tg_id == user_tg_id).get()
        user.is_admin = True
        user.save()
        return True
    User.create(user_tg_id=user_tg_id, username=username, is_admin=True)
    return True


def user_is_admin(user_tg_id: str) -> bool:
    if User.select().where(User.user_tg_id == user_tg_id).count() == 0:
        return False
    user = User.select().where(User.user_tg_id == user_tg_id).get()
    return user.is_admin
