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
