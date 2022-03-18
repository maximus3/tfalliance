import peewee

from status_code import StatusCode
from models import AllThemes


def add_new_theme(theme_name, tg_bot_token, bot_nick):  # TODO
    if AllThemes.select().where(AllThemes.theme_name == theme_name).count() > 0:
        return StatusCode.THEME_ALREADY_EXISTS, None
    theme = None
    try:
        theme = AllThemes.create(theme_name=theme_name, tg_bot_token=tg_bot_token, bot_nick=bot_nick)
    except peewee.IntegrityError as exc:
        if str(exc).startswith('UNIQUE'):
            return StatusCode.THEME_ALREADY_EXISTS, None
        else:
            return StatusCode.ERROR_IN_ADD_TO_DATABASE, None
    except Exception:
        return StatusCode.ERROR_IN_ADD_TO_DATABASE, None
    return StatusCode.OK, theme
