from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    CharField,
    AutoField,
    ForeignKeyField,
    DateTimeField,
)

from config_data.config import DB_PATH

db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField()
    username = CharField()
    first_name = CharField()


class Choice(BaseModel):
    choice_id = AutoField()
    user = ForeignKeyField(User, backref='choices')
    city = CharField()
    command = CharField()
    choice = CharField()
    date_of_request = DateTimeField()
    date_of_visit = CharField()
    sort = CharField()


async def create_models():
    db.create_tables(BaseModel.__subclasses__())
