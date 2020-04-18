from playhouse.postgres_ext import Model
from playhouse.shortcuts import model_to_dict

from back.core import db, config

class BaseModel(Model):
    def get_small_data(self):
        return model_to_dict(self, recurse=False, backrefs=False)

    class Meta:
        database = db
        schema = config['database']['schema']
