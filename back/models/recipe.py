from peewee import *
from playhouse.postgres_ext import ArrayField
from .base_model import BaseModel
from .wine import Wine
from .area import Area

from back.core import db

class Category(BaseModel):
    id = AutoField()
    name = CharField()

class Recipe(BaseModel):
    id = AutoField()
    name = TextField()
    ingredients = ArrayField(TextField, null=True)
    preparation = ArrayField(TextField, null=True)
    image = TextField(null=True)
    category = ForeignKeyField(Category, backref='recipes')

    def get_data(self):
        data = self.get_small_data()
        data['wines'] = [w.get_small_data() for w in self.wines]
        return data

    def modify_ing(self):
        return Recipe.update(ingredients=[self.name]).where(Recipe.id==self.id).execute()

class WineRecipe(BaseModel):
    id = AutoField()
    wine = ForeignKeyField(Wine, backref='recipes')
    recipe = ForeignKeyField(Recipe, backref='wines')

class AreaRecipe(BaseModel):
    id = AutoField()
    area = ForeignKeyField(Area, backref='recipes')
    recipe = ForeignKeyField(Recipe, backref='areas')

with db:
    Category.create_table(safe=True)
    Recipe.create_table(safe=True)
    WineRecipe.create_table(safe=True)
    AreaRecipe.create_table(safe=True)