import peewee
import config


class BaseModel(peewee.Model):
    class Meta:
        database = config.DB


class User(BaseModel):
    id = peewee.IntegerField()
    email = peewee.TextField()
    password = peewee.TextField()
    anket_id = peewee.IntegerField()


class Anket(BaseModel):
    id = peewee.IntegerField()
    surname = peewee.TextField()
    name = peewee.TextField()
    secondname = peewee.TextField()


class Place(BaseModel):
    id = peewee.IntegerField()
    added_to_favorites = peewee.IntegerField()


class UserPlaces(BaseModel):
    id = peewee.IntegerField()
    user_id = peewee.IntegerField()
    place_id = peewee.IntegerField()
    comment = peewee.TextField()
