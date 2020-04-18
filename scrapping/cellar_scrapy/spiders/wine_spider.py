import scrapy 
from scrapy.loader import ItemLoader
from scrapping.cellar_scrapy.items import WineDeciderItem, HachetteWineItem, RecipeItem, WineItem


class WineDeciderSpider(scrapy.Spider):
    name='winedecider'

    #start_urls = ['http://www.winedecider.com/fr/find2/elargie.php?cbResetParam=1&keyword=+clo+fee+1994+&keywordfrom=clos+des+fees+1994']

    def __init__(self, query=None, *args, **kwargs):
        super(WineDeciderSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://www.winedecider.com/fr/find/recherche.php?cbResetParam=1&keyword={}'.format(query)]

    def parse(self, response):
        wines = response.css('table.table > tr')
        for wine in wines:
            loader = ItemLoader(item=WineDeciderItem(), selector=wine)
            loader.add_css('maturity', css='td.cbResultSetTableCell > img::attr(src)')
            loader.add_css('winery_name', css='td.cbResultSetTableCell > h3::text')
            loader.add_css('wine_name', css='td.cbResultSetTableCell::text')
            loader.add_css('vintage', css='td:nth-child(3) h3::text')
            loader.add_css('mark', css='td:nth-child(5) ::text')
            yield loader.load_item()
            
            #wine_item = loader.load_item()

            # wine_url = wine.css('td:last-child > a::attr(href)').get()
            # yield response.follow(wine_url, callback=self.parse_wine, meta={'wine_item':wine_item})

            # yield {
            #     'maturite': wine.css('td.cbResultSetTableCell img::attr(src)').extract(),
            #     'wine_name':wine.css('td.cbResultSetTableCell h3::text').get(),
            #     'domain_name':wine.css('td.cbResultSetTableCell::text').get(),
            #     'vintage':wine.css('td h3:nth-child(2) ::text').get(),
            #     'mark': wine.css('td h3::text')[2].get() if len(wine.css('td::text').getall())>3 else None
            # }
    # def parse_wine(self, response):
    #     wine_item = response.meta['wine_item']
    #     loader = ItemLoader(item=wine_item, selector=response)
    #     print(response.css('div.col-md-5 > img::attr(src)').extract())
    #     loader.add_css('wine_picture', css='div > div > img::attr(src)')
    #     print(response.css('#content section:nth-child(3)').get())
    #     loader.add_css('grape_types', css='#content_fiche_vin > ul > li:nth-child(3) ::text')
    #     loader.add_css('consumption_advise', css='#content_fiche_vin > ul > li:nth-child(4) ::text')
        # yield loader.load_item()

class HachetteWineSpider(scrapy.Spider):
    name='hachette'

    def __init__(self, query=None, *args, **kwargs):
        super(HachetteWineSpider, self).__init__(self, *args, **kwargs)
        self.start_urls = ['https://www.hachette-vins.com/recherche/{}'.format(query)]

    def parse(self, response):
        wines = response.css('div.panels div.block')
        for i,wine in enumerate(wines):
            if i==0:
                loader = ItemLoader(item=HachetteWineItem(), selector=wine)
                loader.add_css('wine_name', css='div.content div.sub-title h2::text')
                loader.add_css('region_name', css='div.content div.add span:first-child ::text')
                loader.add_css('area_name', css='div.content div.add span:last-child ::text')
                loader.add_css('default_name', css='div.content div.title span ::text')
                # loader.add_css('wine_url', css='div.content div.title a::attr(href)')
                wine_item = loader.load_item()
                # yield {
                #     'domain_name':wine.css('div.content div.title a::text').get(),
                #     'wine_name':wine.css('div.content div.sub-title h2::text').get(),
                # }
                wine_url = wine.css('div.content div.title a::attr(href)').get()
                yield response.follow(wine_url, callback=self.parse_wine, meta={'wine_item':wine_item})

    def parse_wine(self, response):
        wine_item = response.meta['wine_item']
        loader = ItemLoader(item=wine_item, selector=response)
        loader.add_xpath('winery_description', '//div[@class="description"]//div[@class="content"]//span//text()[re:test(., "\w+")]')
        #loader.add_css('description', css='div.description div.content span')
        loader.add_css('winery_name', css='div.detail-du-vin div.blocks-pro div:first-child div.sub-title h3 span ::text')
        # loader.add_css('area_name', css='div.detail-du-vin div.blocks-pro div:nth-child(2) div.sub-title h3 ::text')
        # loader.add_css('default_name', css='div.detail-product div.title h1 span ::text')
        yield loader.load_item()

    def parse_recipe(self, response):
        recipe_item = response.meta['recipe_item']
        ingredients = response.css('div.ingredient li')
        for ingredient in ingredients:
            loader = ItemLoader(item=recipe_item, selector=ingredient)
            loader.add_css('recipes_ingredients', css='::text')
            loader.load_item()
        prepa = response.css('div.preparation li')
        for step in prepa:
            loader = ItemLoader(item=recipe_item, selector=step)
            loader.add_css('recipes_prepa', css='div > p ::text')
            loader.load_item()
        loader = ItemLoader(item=recipe_item, selector=ingredient)
        loader.add_value('recipes_ingredients','stop')
        loader.add_value('recipes_prepa', 'stop')

class RecipeSpider(scrapy.Spider):
    name='recipe'

    def __init__(self, query=None, *args, **kwargs):
        super(RecipeSpider, self).__init__(self, *args, **kwargs)
        self.start_urls = ['https://www.hachette-vins.com{}'.format(query)]

    def parse(self, response):
        loader = ItemLoader(item=RecipeItem(), selector=response)
        loader.add_css('recipe_name', css='div.container h1.main-title span ::text')
        loader.add_css('recipe_image', css='div.container div.product-area div.image ::attr(src)')
        ingredient_loader = loader.nested_css('div.ingredient li')
        ingredient_loader.add_css('recipe_ingredients', css='::text')
        prepa_loader = loader.nested_css('div.preparation li')
        prepa_loader.add_css('recipe_prepa', css='div > p ::text')
        yield loader.load_item()

class WineSpider(scrapy.Spider):
    name='wine'

    def __init__(self, query=None, *args, **kwargs):
        super(WineSpider, self).__init__(self, *args, **kwargs)
        self.start_urls = ['https://www.hachette-vins.com{}'.format(query)]

    def parse(self, response):
        loader = ItemLoader(item=WineItem(), selector=response)
        loader.add_xpath('winery_description', '//div[@class="description"]//div[@class="content"]//span//text()[re:test(., "\w+")]')
        loader.add_css('winery_name', css='div.detail-du-vin div.blocks-pro div:first-child div.sub-title h3 span ::text')
        
        ## No need because the recipes are already imported
        # nested_loader = loader.nested_css('div#extrait div.item')
        # nested_loader.add_css('recipes_urls', css='a::attr(href)')
        # nested_loader.add_css('recipes_names', css='a span:nth-child(2) ::text')
        yield loader.load_item()


        






