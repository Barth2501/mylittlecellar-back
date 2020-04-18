from back.core import db
from back.models.region import Region, RegionInfo
from back.models.area import Area, AreaInfo, AreaGrape, Grape, GrapeSynonym


class RegionPipeline(object):

    def process_item(self, item, spider):
        print(item)
        if 'region_name' in item.keys():
            region = Region.get_or_none(name=item['region_name'])
            if not region:
                region = Region.create(name=item['region_name'])
            region_info = RegionInfo.get_or_none(region=region)
            if not region_info:
                true_item = {}
                for key in item.keys():
                    true_item[key] = ''
                    for elem in item[key]:
                        if elem!='':
                            true_item[key] += elem
                RegionInfo.create(region=region, **true_item)
        if 'area_name' in item.keys():
            area = Area.get_or_none(name=item['area_name'])
            if not area:
                area = Area.create(name=item['area_name'])
            if area:
                region = Region.get_or_none(name=item['r_name'])
                if region:
                    area.modify_region(region)
                area_info = AreaInfo.get_or_none(area=area)
                if not area_info:
                    eye=''
                    mouth=''
                    nose=''
                    food=''
                    if 'detail' in item.keys():
                        for i,detail in enumerate(item['detail']):
                            if detail == 'Oeil:':
                                eye = item['detail'][i+1]
                            if detail == 'Nez:':
                                nose = item['detail'][i+1]
                            if detail == 'Bouche:':
                                mouth = item['detail'][i+1]
                            if detail == 'Mets vins:':
                                food = item['detail'][i+1]                        
                    true_kp = ''
                    if 'keep_advise' in item.keys():
                        for kp in item['keep_advise']:
                            if kp!='':
                                true_kp += kp
                    true_desc = ''
                    if 'description' in item.keys():
                        for desc in item['description']:
                            if desc!='':
                                true_desc += desc
                    photo = ''
                    if 'photo' in item.keys():
                        photo = item['photo']
                    AreaInfo.create(area=area, eye=eye, nose=nose, mouth=mouth, food=food, description=true_desc, keep_advise=true_kp, photo=photo)
                if 'main_grapes' in item.keys():
                    for grape_name in item['main_grapes']:
                        grape = Grape.get_or_none(name=grape_name.upper())
                        if grape:
                            area_grape = AreaGrape.get_or_none(grape=grape, area=area)
                            if not area_grape:
                                AreaGrape.create(grape=grape, area=area)
            
class GrapesPipeline(object):
    def process_item(self, item, spider):
        print(item)
        grape = Grape.get_or_none(name=item['name'])
        if not grape:
            true_desc = ''
            for desc in item['description']:
                if desc != '':
                    true_desc += desc
            grape = Grape.create(name=item['name'], color=item['color'], description=true_desc)
            if 'similar' in item.keys():
                for similar in item['similar']:
                    grape_bis = Grape.get_or_none(name=similar)
                    if grape_bis:
                        grape_synonym = GrapeSynonym.get_or_none(grape_1=grape, grape_2=grape_bis)
                        if not grape_synonym:
                            GrapeSynonym.create(grape_1=grape, grape_2=grape_bis)
