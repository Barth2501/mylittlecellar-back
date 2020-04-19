import crochet
crochet.setup()

from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from scrapping.cellar_scrapy.spiders.wine_spider import WineDeciderSpider, HachetteWineSpider, RecipeSpider, WineSpider
from scrapping.cellar_scrapy.spiders.recipes_spider import RecipesSpider
from scrapping.cellar_scrapy.spiders.region_spider import RegionSpider, GrapeSpider, VinDePaysSpider

from scrapping.cellar_scrapy.pipelines import HachettePipeline, RecipePipeline, WinePipeline, RecipesPipeline, WineDeciderPipeline
## to uncomment if you want to import 
# from back.models.pipelines.hachette_pipelines import RegionPipeline, GrapesPipeline
# from scrapy.utils.project import get_project_settings
# from scrapping.main import wine_decider
import time

app = Flask('scrapping')
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = 'test'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400

CORS(app, resources={r'/*':{'origins':'*'}}, supports_credentials=True)


@app.route('/wine_decider', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        crawl_runner = CrawlerRunner({
            'BOT_NAME' : 'scrapping.cellar_scrapy',
            'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
            'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
            'ROBOTSTXT_OBEY' : False,
            'ITEM_PIPELINES' : {
            'scrapping.cellar_scrapy.pipelines.WineDeciderPipeline': 300,
            },
        })
        post_data = request.get_json()
        print(post_data['query'])
        if post_data['query']!=WineDeciderPipeline.last_query or not WineDeciderPipeline.is_running:
            scrape_with_crochet(query=post_data['query'], spider=WineDeciderSpider,crawl_runner=crawl_runner, pipeline=WineDeciderPipeline)
            WineDeciderPipeline.last_query = post_data['query']
            WineDeciderPipeline.start_time = time.time()

        while not WineDeciderPipeline.items:

            if post_data['query']==WineDeciderPipeline.last_query:
                if time.time() - WineDeciderPipeline.start_time < 5:
                    continue
                else:
                    WineDeciderPipeline.is_running = False
                    return jsonify({'msg':'scrapping stopped'})
            else:
                return jsonify({'msg':'scrapping changed'})

        response_object = {'msg':'scrapping received'}
        response_object['wines'] = WineDeciderPipeline.items
        WineDeciderPipeline.items = []
        return jsonify(response_object)


@app.route('/hachette', methods=['GET','POST'])
def hachette():
    if request.method == 'POST':
        post_data = request.get_json()
        return redirect(url_for('hachette_scrape', query=post_data['query']))

@app.route('/hachette/recipe', methods=['POST'])
def recipe():
    if request.method == 'POST':
        crawl_runner = CrawlerRunner({
            'BOT_NAME' : 'scrapping.cellar_scrapy',
            'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
            'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
            'ROBOTSTXT_OBEY' : False,
            'ITEM_PIPELINES' : {
            'scrapping.cellar_scrapy.pipelines.RecipePipeline': 300,
            },
        })
        post_data = request.get_json()
        scrape_with_crochet(query=post_data['url'], spider=RecipeSpider,crawl_runner=crawl_runner, pipeline=RecipePipeline)
        while not RecipePipeline.items:
            continue
        response_object = RecipePipeline.items
        RecipePipeline.items = None
        response_object['status'] = 'success'
        return jsonify(response_object)

@app.route('/hachette/recipes', methods=['POST'])
def recipes():
    if request.method == 'POST':
        crawl_runner = CrawlerRunner({
            'BOT_NAME' : 'scrapping.cellar_scrapy',
            'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
            'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
            'ROBOTSTXT_OBEY' : False,
            'ITEM_PIPELINES' : {
            'scrapping.cellar_scrapy.pipelines.RecipesPipeline': 300,
            },
        })
        post_data = request.get_json()
        scrape_with_crochet(query=post_data['index'], spider=RecipesSpider,crawl_runner=crawl_runner, pipeline=RecipesPipeline)
        while len(RecipesPipeline.items)<6:
            continue
        response_object = {'status':'success'}
        response_object['recipes'] = RecipesPipeline.items
        RecipesPipeline.items = []
        print(response_object)
        return jsonify(response_object)

@app.route('/hachette/wine', methods=['POST'])
def wine():
    if request.method == 'POST':
        crawl_runner = CrawlerRunner({
            'BOT_NAME' : 'scrapping.cellar_scrapy',
            'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
            'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
            'ROBOTSTXT_OBEY' : False,
            'ITEM_PIPELINES' : {
            'scrapping.cellar_scrapy.pipelines.WinePipeline': 300,
            },
        })
        post_data = request.get_json()
        scrape_with_crochet(query=post_data['url'], spider=WineSpider,crawl_runner=crawl_runner, pipeline=WinePipeline)
        while not WinePipeline.items:
            continue
        response_object = WinePipeline.items
        WinePipeline.items = None
        response_object['status'] = 'success'
        return jsonify(response_object)

@app.route('/hachette/region_area_info', methods=['GET'])
def region_area_info():
    if request.method == 'GET':
        crawl_runner = CrawlerRunner({
            'BOT_NAME' : 'scrapping.cellar_scrapy',
            'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
            'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
            'ROBOTSTXT_OBEY' : False,
            'ITEM_PIPELINES' : {
            'back.models.pipelines.hachette_pipelines.RegionPipeline': 300,
            },
        })
        scrape_with_crochet(spider=RegionSpider, query=None, crawl_runner=crawl_runner, pipeline=RegionPipeline)
        response_object = {'status': 'success'}
        return jsonify(response_object)

@app.route('/hachette/vins_de_pays_info', methods=['GET'])
def vins_de_pays_info():
    if request.method == 'GET':
        crawl_runner = CrawlerRunner({
            'BOT_NAME' : 'scrapping.cellar_scrapy',
            'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
            'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
            'ROBOTSTXT_OBEY' : False,
            'ITEM_PIPELINES' : {
            'back.models.pipelines.hachette_pipelines.RegionPipeline': 300,
            },
        })
        scrape_with_crochet(spider=VinDePaysSpider, query=None, crawl_runner=crawl_runner, pipeline=RegionPipeline)
        response_object = {'status': 'success'}
        return jsonify(response_object)

@app.route('/hachette/grapes', methods=['POST'])
def grapes_info():
    if request.method == 'POST':
        crawl_runner = CrawlerRunner({
            'BOT_NAME' : 'scrapping.cellar_scrapy',
            'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
            'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
            'ROBOTSTXT_OBEY' : False,
            'ITEM_PIPELINES' : {
            'back.models.pipelines.hachette_pipelines.GrapesPipeline': 300,
            },
        })
        post_data = request.get_json()
        for letter in post_data['letters']:
            scrape_with_crochet(spider=GrapeSpider, query=letter, crawl_runner=crawl_runner, pipeline=GrapesPipeline)
        response_object = {'status': 'success'}
        return jsonify(response_object)

@app.route("/h_scrape/<query>")
def hachette_scrape(query):
    crawl_runner = CrawlerRunner({
        'BOT_NAME' : 'scrapping.cellar_scrapy',
        'SPIDER_MODULES' : ['scrapping.cellar_scrapy.spiders'],
        'NEWSPIDER_MODULE' : 'scrapping.cellar_scrapy.spiders',
        'ROBOTSTXT_OBEY' : False,
        'ITEM_PIPELINES' : {
           'scrapping.cellar_scrapy.pipelines.HachettePipeline': 300,
        },
    })
    query = query.replace(' ','%20')
    query += '/all/'
    scrape_with_crochet(query=query, spider=HachetteWineSpider, crawl_runner=crawl_runner, pipeline=HachettePipeline)
    wine_item = None
    start = time.time()
    while not HachettePipeline.items:
        now = time.time()
        if now - start > 15:
            wine_item = 'Not found'
            break
    if not wine_item:
        wine_item = HachettePipeline.items[0]
    response_object = {'status':'success'}
    response_object['wines'] = wine_item
    HachettePipeline.items = []
    return jsonify(response_object)

@crochet.run_in_reactor
def scrape_with_crochet(query,spider,crawl_runner,pipeline):
    dispatcher.connect(pipeline, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(spider, query=query)
    return eventual


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)