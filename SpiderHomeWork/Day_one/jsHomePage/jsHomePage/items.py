# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JsHomePageItem(scrapy.Item):
    # define the fields for your item here like:
    author_name = scrapy.Field()
    article_title = scrapy.Field()
    article_release_time = scrapy.Field()
    article_collection_tag = scrapy.Field()
    article_read_count = scrapy.Field()
    article_comment_count = scrapy.Field()
    article_likeit_count = scrapy.Field()
    article_payit_count = scrapy.Field()
    # pass
