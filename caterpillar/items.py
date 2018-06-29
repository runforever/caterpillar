# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class House(scrapy.Item):
    '''
    房源信息
    '''
    source_url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    payment = scrapy.Field()
    house_type = scrapy.Field()
    house_community = scrapy.Field()
    region = scrapy.Field()
    address = scrapy.Field()
    desc = scrapy.Field()
    imgs = scrapy.Field()
