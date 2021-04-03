from model import *
from config import DB as db

db.connect()
db.drop_tables([User, Anket, Place])
db.create_tables([User, Anket, Place])
db.close()
