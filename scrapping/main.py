from cellar_scrapy.spiders.wine_spider import WineDeciderSpider, HachetteWineSpider, RecipeSpider
from cellar_scrapy.spiders.recipes_spider import RecipesSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from cellar_scrapy.pipelines import HachettePipeline, RecipePipeline, RecipesPipeline

def wine_decider(query):
    process = CrawlerProcess(get_project_settings())
    # query = 'lancelot pienne'
    words = query.split(' ')
    mod_query = ''
    for word in words:
        mod_query += word + '+' 
    process.crawl(WineDeciderSpider, query=mod_query)
    process.start()
    items = MainPipeline.items
    return items

def hachette_vin():
    process = CrawlerProcess(get_project_settings())
    query = 'lancelot pienne'
    query = query.replace(' ','%20')
    query += '/all/'
    process.crawl(HachetteWineSpider, query=query)
    process.start()
    return HachettePipeline.items

def recipe():
    process = CrawlerProcess({'BOT_NAME' : 'cellar_scrapy',
    'SPIDER_MODULES' : ['cellar_scrapy.spiders'],
    'NEWSPIDER_MODULE' : 'cellar_scrapy.spiders',
    'ROBOTSTXT_OBEY' : False,
    'ITEM_PIPELINES' : {
       'cellar_scrapy.pipelines.RecipePipeline': 300,
    },})
    query = 'cuisine-vins/80/daurade-a-la-citronnelle/'
    process.crawl(RecipeSpider, query=query)
    process.start()
    return RecipePipeline.items

def recipes():
    process = CrawlerProcess({'BOT_NAME' : 'cellar_scrapy',
    'SPIDER_MODULES' : ['cellar_scrapy.spiders'],
    'NEWSPIDER_MODULE' : 'cellar_scrapy.spiders',
    'ROBOTSTXT_OBEY' : False,
    'ITEM_PIPELINES' : {
       'cellar_scrapy.pipelines.RecipesPipeline': 300,
    },})
    query = 1
    process.crawl(RecipesSpider, query=query)
    process.start()
    return RecipesPipeline.items

items = hachette_vin()
print(items)
for item in items:
    print('here are the items',item)