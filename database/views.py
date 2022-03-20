from .models import AllThemes
from .status_code import StatusCode


def add_new_theme(
    theme_name: str, user_id: str, chat_id: str, start_message: str
) -> StatusCode:
    AllThemes.create(
        theme_name=theme_name,
        start_message=start_message,
        chat_id=chat_id,
        user_id=user_id,
    )
    return StatusCode.OK


def delete_theme_by_chat(chat_id: int) -> bool:
    theme = (
        AllThemes.select().where(AllThemes.chat_id == chat_id).get_or_none()
    )
    if theme:
        theme.delete()
    return True

  
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
