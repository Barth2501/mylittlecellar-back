from back.models import Area, Region, Winery, CellarWine, Wine

def create_area(name:str):
    return Area.create(name=name)

def get_area_info(area_name:str, cellar_id:int):
    area = Area.get_or_none(name=area_name)
    if not area:
        return {'msg':'no area under the name {}'.format(area_name)}
    res = area.get_info_grapes_data()
    res['region'] = Region.get_by_id(area.region).get_small_data()
    relevant_wineries = Winery.select(Winery).from_(CellarWine,Area,Wine,Winery).where(
                            Area.name==area_name,
                            Area.id==Winery.area,
                            Winery.id==Wine.winery,
                            CellarWine.wine==Wine.id,
                            CellarWine.cellar==cellar_id
                        ).group_by(Winery)
    res['winery'] = [winery.get_small_data() for winery in relevant_wineries]
    return res