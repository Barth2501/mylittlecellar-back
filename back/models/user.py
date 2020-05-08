from peewee import *

from back.core import db

from .base_model import BaseModel

class User(BaseModel):
    id = AutoField()
    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()

    def get_data(self):
        data = self.get_small_data()
        user_id = self.id
        data['areas'] = [a.area.get_data(user_id) for a in self.areas]
        return data

with db:
    User.create_table(safe=True)