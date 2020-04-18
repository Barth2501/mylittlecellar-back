# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time


class WineDeciderPipeline(object):
    items = []
    is_running = False
    start_time = 0
    last_query = ''

    def __init__(self):
        WineDeciderPipeline.items = []
        self.ids_seen = set()
        WineDeciderPipeline.is_running = True
        
    def process_item(self, item, spider):
        int_result = {}
        for key in item.keys():
            int_result[key] = item[key]
        WineDeciderPipeline.items.append(int_result)      

class HachettePipeline(object):
    items = []

    def __init__(self):
        HachettePipeline.items = []
    def process_item(self, item, spider):
        int_result = {}

        # vintage_list = re.findall(r'[0-9]{4,}',item['wine_name'])
        # if len(vintage_list) > 0:
        #     int_result['vintage'] = vintage_list[0]
        #     item['wine_name'] = item['wine_name'].strip(vintage_list[0])
        for key in item.keys():
            int_result[key] = item[key]
        if int_result['wine_name'] == '':
            int_result['wine_name'] = item['default_name']
        HachettePipeline.items.append(int_result)
        
class RecipePipeline(object):
    items = None

    def __init__(self):
        RecipePipeline.items = None
        self.ids_seen = set()

    def process_item(self, item, spider):
        int_result = {}
        for key in item.keys():
            int_result[key] = item[key]
        RecipePipeline.items = int_result

class RecipesPipeline(object):
    items = []

    def __init__(self):
        RecipesPipeline.items = []
        self.ids_seen = set()

    def process_item(self, item, spider):
        int_result = {}
        for key in item.keys():
            int_result[key] = item[key]
        RecipesPipeline.items.append(int_result)

class WinePipeline(object):
    items = None

    def __init__(self):
        WinePipeline.items = None
        self.ids_seen = set()

    def process_item(self, item, spider):
        int_result = {}
        int_result['recipes'] = {}
        for key in item.keys():
            if key in ['recipes_names', 'recipes_urls']:
                int_result['recipes'][key] = item[key]
            else:
                int_result[key] = item[key]
        WinePipeline.items = int_result
