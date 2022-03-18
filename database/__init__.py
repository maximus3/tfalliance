from pathlib import Path

from .models import DATABASE_NAME, AllThemes, Theme, User, database


def create_tables():
    if Path(DATABASE_NAME).exists():
        return False
    with database:
        database.create_tables([AllThemes, Theme, User])
    return True


create_tables()
