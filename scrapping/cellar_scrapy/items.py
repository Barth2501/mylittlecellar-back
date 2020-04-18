# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def parse_image(text):
    text = text[-7:-4]
    if text == 'B1f':
        return 'Blanc/à garder'
    elif text == 'B2f':
        return 'Blanc/à boire ou à garder'
    elif text == 'B3f':
        return 'Blanc/à boire'
    elif text == 'R1f':
        return 'Rouge/à garder'
    elif text == 'R2f':
        return 'Rouge/à boire ou à garder'
    elif text == 'R3f':
        return 'Rouge/à boire'

def parse_vintage(text):
    return int(text)

def convert_mark(text):
    nb1, nb2 = text.split('/')
    return int(nb1)/int(nb2)

def parse_description(text):
    text = text.strip()
    text = text.replace(u'\xa0',' ')
    return text

def parse_grape_color(text):
    if text[-1]=='1':
        return 'Rouge'
    elif text[-1]=='2':
        return 'Blanc'


class WineDeciderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    maturity = scrapy.Field(
        input_processor=MapCompose(parse_image),
        output_processor=TakeFirst()
    )
    wine_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    winery_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    vintage = scrapy.Field(
        input_processor=MapCompose(parse_vintage),
        output_processor=TakeFirst()
    )
    mark = scrapy.Field(
        input_processor=MapCompose(convert_mark),
        output_processor=TakeFirst()
    )

class HachetteWineItem(scrapy.Item):
    wine_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    default_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    region_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    area_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    # wine_url = scrapy.Field(
    #     input_processor=MapCompose(str.strip),
    #     output_processor=TakeFirst()
    # )
    winery_description = scrapy.Field(
        input_processor=MapCompose(parse_description),
    )
    winery_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )

class RecipeItem(scrapy.Item):
    recipe_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    recipe_image = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    recipe_ingredients = scrapy.Field(
        input_processor=MapCompose(parse_description),
    )
    recipe_prepa = scrapy.Field(
        input_processor=MapCompose(parse_description),
    )

class WineItem(scrapy.Item):
    winery_description = scrapy.Field(
        input_processor=MapCompose(parse_description),
    )
    winery_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    recipes_urls = scrapy.Field()
    recipes_names = scrapy.Field(
        input_processor=MapCompose(str.strip)
    )

class RecipesItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    image = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    areas = scrapy.Field(
        input_processor=MapCompose(str.strip)
    )
    category_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    ingredients = scrapy.Field(
        input_processor=MapCompose(parse_description),
    )
    preparation = scrapy.Field(
        input_processor=MapCompose(parse_description),
    )
    
class RegionItem(scrapy.Item):
    region_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(parse_description)
    )
    wine_style = scrapy.Field(
        input_processor=MapCompose(parse_description)
    )
    history = scrapy.Field(
        input_processor=MapCompose(parse_description)
    )
    weather_and_soil = scrapy.Field(
        input_processor=MapCompose(parse_description)
    )
    region_map = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )

class AreaItem(scrapy.Item):
    area_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    r_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(parse_description)
    )
    main_grapes = scrapy.Field(
        input_processor=MapCompose(str.strip)
    )
    photo = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    keep_advise = scrapy.Field(
        input_processor=MapCompose(str.strip)
    )
    detail = scrapy.Field(
        input_processor=MapCompose(parse_description)
    )

class GrapeItem(scrapy.Item):
    name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(parse_description)
    )
    color = scrapy.Field(
        input_processor=MapCompose(parse_grape_color),
        output_processor=TakeFirst()
    )
    similar = scrapy.Field(
        input_processor=MapCompose(str.strip),
    )

