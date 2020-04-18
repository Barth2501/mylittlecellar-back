import scrapy 
from scrapy.loader import ItemLoader
from scrapping.cellar_scrapy.items import RecipesItem

class RecipesSpider(scrapy.Spider):
    name='recipes_import'

    def __init__(self, query=None, *args, **kwargs):
        super(RecipesSpider, self).__init__(self, *args, **kwargs)
        self.start_urls = ['https://www.hachette-vins.com/recherche//accord/{}'.format(query)]

    def parse(self, response):
        recipes = response.css('div.panels div.history-area-full div.block')
        for i,recipe in enumerate(recipes):
            if i < 6:
                recipe_url = recipe.css('div.content > div.title a::attr(href)').get()
                yield response.follow(recipe_url+'#recette', callback=self.parse_recipe)

    def parse_recipe(self,response):
        loader = ItemLoader(item=RecipesItem(), selector=response)
        loader.add_css('name', css='div.container h1.main-title span ::text')
        loader.add_css('category_name', css='div.main-content li:nth-child(3) a span ::text')
        ingredient_loader = loader.nested_css('div.ingredient-area div.ingredient li')
        ingredient_loader.add_css('ingredients', css='::text')

        ## Uncomment if we decided to show the recipe 
        # prepa_loader = loader.nested_css('div.preparation li')
        # prepa_loader.add_css('preparation', css='div > p ::text')
        area_loader = loader.nested_css('div.name-area div.item')
        area_loader.add_css('areas', css='div.title a ::text')
        # prepa_url = response.css('div.recipe-info div.action a ::attr(href)')
        yield loader.load_item()