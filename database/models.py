from peewee import (
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
    theme_name = CharField()
    start_message = CharField()
    chat_id = CharField(unique=True)
    user_id = CharField()
    secret = CharField(unique=True)


class Theme(BaseModel):
    msg_uid = IntegerField(primary_key=True)
    theme = ForeignKeyField(
        AllThemes, related_name='theme', on_delete='CASCADE'
    )
    message = CharField()
    user_id = CharField()
    chat_id = CharField()
    message_id = CharField()
    timestamp = DateTimeField()
