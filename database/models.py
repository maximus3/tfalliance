from peewee import (
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
)

from config import DATABASE_NAME

database = SqliteDatabase(DATABASE_NAME)


class BaseModel(Model):
    class Meta:
        database = database


class AllThemes(BaseModel):
    theme_uid = IntegerField(primary_key=True)
    theme_name = CharField(unique=True)
    tg_bot_token = CharField()
    bot_nick = CharField()


class User(BaseModel):
    user_tg_id = CharField()
    user_name = CharField()
    is_admin = BooleanField(default=False)


class Theme(BaseModel):
    msg_uid = IntegerField(primary_key=True)
    theme_uid = ForeignKeyField(AllThemes, related_name='theme')
    message = CharField()
    user = ForeignKeyField(User, related_name='theme')
    completed = BooleanField()
    timestamp = DateTimeField()
