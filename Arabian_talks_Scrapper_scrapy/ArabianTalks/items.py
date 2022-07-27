# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArabiantalksItem(scrapy.Item):
    # define the fields for your item here like:
    categories_url = scrapy.Field()
    categories_title = scrapy.Field()
    companies_registered = scrapy.Field()
    pass
