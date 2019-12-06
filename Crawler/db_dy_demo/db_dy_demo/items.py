# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DbDyDemoItem(scrapy.Item):
    directors =scrapy.Field()
    rate =scrapy.Field()
    cover_x =scrapy.Field()
    star =scrapy.Field()
    title =scrapy.Field()
    url =scrapy.Field()
    casts =scrapy.Field()
    cover =scrapy.Field()
    id =scrapy.Field()
    cover_y =scrapy.Field()