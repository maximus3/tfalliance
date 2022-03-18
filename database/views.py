import peewee

from .models import AllThemes
from .status_code import StatusCode


def add_new_theme(
    theme_name: str, tg_bot_token: str, bot_nick: str
) -> StatusCode:  # TODO
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
