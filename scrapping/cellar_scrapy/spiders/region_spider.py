import scrapy 
from scrapy.loader import ItemLoader
from scrapping.cellar_scrapy.items import RegionItem, AreaItem, GrapeItem


class RegionSpider(scrapy.Spider):
    name='regionspider'

    def __init__(self, query=None, *args, **kwargs):
        super(RegionSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['https://www.hachette-vins.com/tout-sur-le-vin/regions-vins/']

    def parse(self, response):
        regions = response.css('div.news-area div.items div.item')
        for region in regions:
            region_url = region.css('div.overlay a ::attr(href)').get()
            yield response.follow(region_url, callback=self.parse_region)

    def parse_region(self, response):
        region_loader = ItemLoader(item=RegionItem(), selector=response)
        region_name = response.css('div.tab-area h2 strong ::text').get()
        region_loader.add_css('region_name', css='div.tab-area h2 strong ::text')
        region_loader.add_css('description', css='div.col-md-8 > div.description > p ::text')
        region_loader.add_css('wine_style', css='div.product-area div.description > p ::text')
        region_loader.add_css('history', css='div.tab-2 div.description p ::text')   
        region_loader.add_css('weather_and_soil', css='div.tab-3 div.description p ::text')
        region_loader.add_css('region_map', css='div.map > a ::attr(href)')
        yield region_loader.load_item()

        areas = response.css('div.items div.item div.info li')
        for area in areas:
            area_url = area.css('a ::attr(href)').get()
            area_loader = ItemLoader(item=AreaItem(), selector=area)
            area_loader.add_css('area_name', css='a ::text')
            area_loader.add_value('r_name', region_name)
            area_item = area_loader.load_item()
            yield response.follow(area_url, callback=self.parse_area, meta={'area_item':area_item})

    def parse_area(self, response):
        area_item = response.meta['area_item']
        area_loader = ItemLoader(item=area_item, selector=response)
        area_loader.add_xpath('description', '//div[@class="col-md-8"]/div[@class="description"]//text()[re:test(., "\w+")]')
        area_loader.add_css('main_grapes', css='div.info div.address a ::text')
        area_loader.add_css('photo', css='div.product-area div.image img ::attr(src)')
        area_loader.add_css('keep_advise', css='div.info div.mobile-half div.meta:nth-child(2) div.address ::text')
        area_loader.add_css('detail', css='div.content > div.description ::text')
        yield area_loader.load_item()

class GrapeSpider(scrapy.Spider):
    name='grapespider'

    def __init__(self, query=None, *args, **kwargs):
        super(GrapeSpider, self).__init__(self, *args, **kwargs)
        self.start_urls = ['https://www.hachette-vins.com/tout-sur-le-vin/cepages-vins/{}/'.format(query)]

    def parse(self, response):
        grapes = response.css('div.items div.item')
        for grape in grapes:
            grape_loader = ItemLoader(item=GrapeItem(), selector=grape)
            grape_loader.add_css('name', css='div.title a ::text')
            grape_loader.add_css('color', css='div.title i ::attr(class)')
            grape_loader.add_css('description', css='div.description:nth-child(2) ::text')
            grape_loader.add_css('similar', css='div.description:nth-child(3) a ::text')
            yield grape_loader.load_item()

class VinDePaysSpider(scrapy.Spider):
    name='vin_de_pays_spider'

    def __init__(self, *args, **kwargs):
        super(VinDePaysSpider, self).__init__(self, *args, **kwargs)
        self.start_urls = ['https://www.hachette-vins.com/tout-sur-le-vin/regions-vins/115/vins-de-pays/']

    def parse(self, response):
        regions = response.css('div.fiche-region-area div.items div.item')
        description = response.css('div.col-md-8 > div.description > p ::text').get()
        wine_style = response.css('div.product-area div.description > p ::text').get()
        history = response.css('div.tab-2 div.description p ::text').get()
        weather_and_soil = response.css('div.tab-3 div.description p ::text').get()
        region_map = response.css('div.map > a ::attr(href)').get()
        for region in regions:
            region_loader = ItemLoader(item=RegionItem(), selector=region)
            region_name = region.css('div.title ::text').get()
            region_loader.add_value('region_name', region_name)
            region_loader.add_value('description', description)
            region_loader.add_value('wine_style', wine_style)
            region_loader.add_value('history', history)   
            region_loader.add_value('weather_and_soil', weather_and_soil)
            region_loader.add_value('region_map', region_map)
            yield region_loader.load_item()

            areas = region.css('div.info li')
            for area in areas:
                area_loader = ItemLoader(item=AreaItem(), selector=area)
                area_loader.add_value('r_name', region_name)
                area_loader.add_css('area_name', css='a ::text')
                area_item = area_loader.load_item()

                area_url = area.css('a ::attr(href)').get()
                yield response.follow(area_url, callback=self.parse_area, meta={'area_item':area_item})

    def parse_area(self, response):
        area_item = response.meta['area_item']
        area_loader = ItemLoader(item=area_item, selector=response)
        area_loader.add_xpath('description', '//div[@class="col-md-8"]/div[@class="description"]//text()[re:test(., "\w+")]')
        area_loader.add_css('main_grapes', css='div.info div.address a ::text')
        area_loader.add_css('photo', css='div.product-area div.image img ::attr(src)')
        area_loader.add_css('keep_advise', css='div.info div.mobile-half div.meta:nth-child(2) div.address ::text')
        area_loader.add_css('detail', css='div.content > div.description ::text')
        yield area_loader.load_item()