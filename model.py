import peewee
import config


class BaseModel(peewee.Model):
    class Meta:
        database = config.DB


class User(BaseModel):
    id = peewee.IntegerField()
    email = peewee.TextField()
    password = peewee.TextField()
