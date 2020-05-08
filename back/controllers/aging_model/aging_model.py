import pandas as pd
import os
from back.models.area import AreaVintage, Area, AreaDetail
from peewee import fn

def aging_model(vintage, age_max, age_min, rank, l=20):
    # period where we will have the evolution
    # need to be bigger than age_max
    period = 2020+age_max+l-vintage
    res = [0 for i in range(period)]
    left = age_min
    right = age_max
    # linear function with the rank in param
    top = int(rank*(age_max-age_min)/10 + age_min)
    print(rank, left, right, top)
    res[right] = res[left] = 50
    res[top] = 100
    for i in range(0,left):
        res[i] = round(50*(i/left)**2)
    for i in range(left,top):
        res[i] = round(-50*((i-top)/(left-top))**2 +100)
    for i in range(top,right):
        res[i] = round(-50*((i-top)/(right-top))**2 +100)
    for i in range(right,period):
        res[i] = round(50*((i-period)/(right-period))**2)
    # we only want the score of the year to come (default 20 years)
    res = res[2020-vintage:2020-vintage+l+1]
    # we give the score by 3 years
    scores_list = [res[i] for i in range(0,len(res),3)]
    list_of_years = [2020+3*i for i in range(len(scores_list))]
    return scores_list, list_of_years

def import_csv():
    df = pd.read_csv('back/controllers/aging_model/age_des_vins_v4.csv', header=0, names=['area_name','cru','age_min','age_max','t_min','t_max','glass_type','comments','color'])
    count = 0
    for info in df.itertuples():
        area = Area.select().where(fn.Upper(Area.name)==info.cru.upper())
        if area.exists():
            area = area.get()
            area_detail = AreaDetail.get_or_none(area=area, color=info.color)
            if not area_detail:
                AreaDetail.create(area = area, color=info.color, age_min=info.age_min, age_max=info.age_max, comments=info.comments, t_min=info.t_min, t_max=info.t_max, glass_type=info.glass_type)
        area = Area.select().where(fn.Upper(Area.name)==info.area_name.upper())
        if area.exists():
            area = area.get()
            area_detail = AreaDetail.get_or_none(area=area, color=info.color)
            if not area_detail:
                AreaDetail.create(area=area,  color=info.color, age_min=info.age_min, age_max=info.age_max, comments=info.comments, t_min=info.t_min, t_max=info.t_max, glass_type=info.glass_type)
    return {'msg':'done'}