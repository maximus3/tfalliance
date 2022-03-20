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


class UserChat(BaseModel):
    user_chat_uid = IntegerField(primary_key=True)
    theme = ForeignKeyField(
        AllThemes, related_name='theme', on_delete='CASCADE'
    )
    chat_id = CharField(unique=True)
    user_id = CharField()
    username = CharField()


class Messages(BaseModel):
    msg_uid = IntegerField(primary_key=True)
    theme = ForeignKeyField(
        AllThemes, related_name='theme', on_delete='CASCADE'
    )
    user_chat = ForeignKeyField(
        UserChat, related_name='user_chat', on_delete='CASCADE'
    )
    text = CharField()
    message_id = CharField()
    timestamp = DateTimeField()
