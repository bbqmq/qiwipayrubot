from peewee import *

db = SqliteDatabase('data/database/database.db')


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db


class User(BaseModel):
    userId = IntegerField(unique=True)
    firstName = CharField()
    userName = CharField()
    balance = FloatField()
    requisites = CharField()
    minOutput = IntegerField()
    autoBlock = BooleanField()
    alertBalance = BooleanField()
    regTime = DateField()

    class Meta:
        db_table = 'users'


class OutputLog(BaseModel):
    userId = IntegerField()
    token = TextField()
    sum = FloatField()
    commision = FloatField()

    class Meta:
        db_table = 'outputLogs'


class Token(BaseModel):
    userId = IntegerField()
    number = CharField()
    token = TextField(unique=True)
    lastBalance = FloatField()

    class Meta:
        db_table = 'tokens'
