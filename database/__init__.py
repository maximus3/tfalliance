from pathlib import Path

from .models import DATABASE_NAME, AllThemes, Messages, UserChat, database


def create_tables() -> bool:
    if Path(DATABASE_NAME).exists():
        return False
    with database:
        database.create_tables([AllThemes, Messages, UserChat])
    return True


create_tables()
