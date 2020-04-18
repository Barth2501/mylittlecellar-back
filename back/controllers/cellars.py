from back.models import Cellar

def create_cellar(user:int, name:str):
    return Cellar.create(user=user, name=name).get_small_data()
    