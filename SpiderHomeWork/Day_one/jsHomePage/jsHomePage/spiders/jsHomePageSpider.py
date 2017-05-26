# -*- coding: utf-8 -*-

import scrapy
from jsHomePage.items import JsHomePageItem

class JshomepagespiderSpider(scrapy.Spider):
    name = "jsHomePageSpider"
    # allowed_domains = ["jianshu.com"]
    start_urls = ['http://www.jianshu.com/', ]

    def parse(self, response):
        jsHomePageItem = JsHomePageItem()
        for article in response.css('div.content'):
            jsHomePageItem['author_name'] = article.css(
                'a.blue-link::text').extract_first()
            jsHomePageItem['article_title'] = article.css(
                'a.title::text').extract_first()
            jsHomePageItem['article_release_time'] = article.css(
                'span.time::attr(data-shared-at)').extract_first()
            isCollectionTag = True if article.css(
                'a.collection-tag') else False
            if isCollectionTag:
                jsHomePageItem['article_collection_tag'] = article.css(
                    'a.collection-tag::text').extract_first()
                jsHomePageItem['article_read_count'] = article.css(
                    'div.meta > a')[1].css('::text').extract()[-1].strip()
                jsHomePageItem['article_comment_count'] = article.css(
                    'div.meta > a')[-1].css('::text').extract()[-1].strip()
            else:
                jsHomePageItem['article_collection_tag'] = 'None'
                jsHomePageItem['article_read_count'] = article.css(
                    'div.meta > a')[0].css('::text').extract()[-1].strip()
                jsHomePageItem['article_comment_count'] = article.css(
                    'div.meta > a')[1].css('::text').extract()[-1].strip()
            jsHomePageItem['article_likeit_count'] = article.css(
                'div.meta > span::text').extract_first()
            isPayitCount = True if article.css(
                'i.iconfont.ic-list-money') else False
            if isPayitCount:
                jsHomePageItem['article_payit_count'] = article.css(
                    'div.meta > span::text').extract()[1]
            yield jsHomePageItem
