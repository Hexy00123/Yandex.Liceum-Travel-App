from model import *
from config import DB as db

db.connect()
db.drop_tables([User])
db.create_tables([User])
db.close()
