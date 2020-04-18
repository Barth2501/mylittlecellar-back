from back.models.winery import Winery
from back.models.region import Region
from back.models.cellar import Cellar
from back.models.area import Area
from back.models.wine import Wine, CellarWine

def create_winery(name:str, area, description:str=''):
    return Winery.create(name=name, area=area, description= description)
    # region = Region.get_or_none(name=region_name)
    # if not region:
    #     region = Region.create(name=region_name)
    # area = Area.get_or_none(name=area_name)
    # if not area:
    #     area = Area.create(name=area_name, region=region)
    # else:
    #     area.modify_region(region=region)
    # if len(name)>len(default_name):
    #     return Winery.create(name=name, description=description, area=area)
    # else:
    #     return Winery.create(name=default_name, description=description, area=area)

def get_winery_info(id:int, cellar_id:int):
    winery = Winery.get_by_id(id)
    if not winery:
        return {'msg':'no winery has the id {}'.format(id)}
    res = winery.get_small_data()
    area = Area.get_by_id(winery.area)
    res['area'] = area.get_small_data()
    res['region'] = Region.get_by_id(area.region).get_small_data()
    relevant_wines = Wine.select().from_(CellarWine,Wine).where(CellarWine.cellar==cellar_id, Wine.winery==id, Wine.id==CellarWine.wine)
    res['wines'] = [wine.get_data_number(cellar_id) for wine in relevant_wines]
    return res