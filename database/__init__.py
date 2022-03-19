from pathlib import Path

from .models import DATABASE_NAME, AllThemes, Theme, database


def create_tables() -> bool:
    if Path(DATABASE_NAME).exists():
        return False
    with database:
        database.create_tables([AllThemes, Theme])
    return True


create_tables()
