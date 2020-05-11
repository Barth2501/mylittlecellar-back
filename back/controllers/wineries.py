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
    return winery.get_names_number(cellar_id)