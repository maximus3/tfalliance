from typing import List, Tuple

import peewee, datetime

import database
from .models import AllThemes, User, Theme
from .status_code import StatusCode


def check_new_theme(theme_name: str) -> StatusCode:
    if (
            AllThemes.select().where(AllThemes.theme_name == theme_name).count()
            > 0
    ):
        return StatusCode.THEME_ALREADY_EXISTS
    return StatusCode.OK


def add_new_theme(
        theme_name: str, tg_bot_token: str, bot_nick: str
) -> StatusCode:
    if check_new_theme(theme_name):
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


def add_message(theme: str, message: str, user: str) -> bool:
    if AllThemes.select().where(AllThemes.theme_name == theme).count() == 0\
            or User.select().where(User.username == user).count() == 0:
        return False
    uid = AllThemes.get(AllThemes.theme_name == theme)
    auth = User.get(User.username == user)
    Theme.create(theme=uid, message=message, user=auth, timestamp=datetime.datetime.now())
    return True


def get_messages(me) -> list:
    if AllThemes.select().where(AllThemes.bot_nick == me).count() == 0:
        return []
    themes = AllThemes.get(AllThemes.bot_nick == me)
    rez = []
    for mes in Theme.select().where(Theme.theme == themes):
        rez.append(mes.message)
    return rez
