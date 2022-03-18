from peewee import *
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

database = SqliteDatabase(BASE_DIR/'bots.db')


class BaseModel(Model):
    class Meta:
        database = database


class AllThemes(BaseModel):
    theme_uid = IntegerField(unique=True, verbose_name='Teleram chat id')
    theme_name = CharField()
    tg_bot_token = CharField()
    bot_nick = CharField()


class Theme(BaseModel):
    msg_uid = IntegerField()
    theme_uid = ForeignKeyField(AllThemes, related_name='theme')
    message = CharField()
    author_tg_id = CharField(max_length=16)
    completed = BooleanField()
    timestamp = DateTimeField()


class Authors(BaseModel):
    author_tg_id = ForeignKeyField(Theme, related_name='author')
    author_name = CharField(max_length=16)


