from back.models import Area, Region, Winery, CellarWine, Wine, Region
import time


def create_area(name:str):
    return Area.create(name=name)

def get_area_info(area_name:str, cellar_id:int):
    area = Area.get_or_none(name=area_name)
    if not area:
        return {'msg':'no area under the name {}'.format(area_name)}
    res = area.get_info_grapes_data()
    res['region'] = Region.get_by_id(area.region).get_data_map()
    # relevant_wineries = Winery.select(Winery).from_(CellarWine,Area,Wine,Winery).where(
    #                         Area.name==area_name,
    #                         Area.id==Winery.area,
    #                         Winery.id==Wine.winery,
    #                         CellarWine.wine==Wine.id,
    #                         CellarWine.cellar==cellar_id
    #                     ).group_by(Winery)
    # res['winery'] = [winery.get_data_number(cellar_id) for winery in relevant_wineries]
    return res

def get_region_info(region_name:str, cellar_id:int):
    region = Region.get_or_none(name=region_name)
    if not region:
        return {'msg':'no region under the name {}'.format(region_name)}
    res = region.get_info_data()
    res['areas'] = [area.get_data_number(cellar_id) for area in region.areas]
    return res

def search_regions_areas(query:str):
    regions = Region.select(Region.name).where(Region.name.contains(query)).dicts()
    areas = Area.select(Area.name).where(Area.name.contains(query)).dicts()
    res = [{"name":q['name'], "type":"region"} for q in regions]
    res += [{'name': q['name'], "type":"area"} for q in areas]
    return res
