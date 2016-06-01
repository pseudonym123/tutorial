#!/usr/bin/env python
# encoding: utf-8

__author__ = 'pseudonym'

import scrapy
from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["69shu.com"]
    start_urls = [
        "http://www.69shu.com/22453/"
    ]

    def parse(self, response):
        for href in response.xpath('//ul[@class="mulu_list"]/li/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        for sel in response.xpath('//td[h1]'):
            header = sel.xpath('h1/text()')
            title = header.extract()[0]
            # id = header.re(u'[\u3007\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u96f6\u767e]+')
            id = response.url[31:]

            contents = sel.xpath('div[@class="yd_text2"]')[0].xpath("text()").extract()
            contents = "".join(contents)
            item = DmozItem()
            item['id'] = id
            item['title'] = title
            item['contents'] = contents
            yield item

    def parse_old(self, response):
        for sel in response.xpath('//ul[@class="mulu_list"]/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            str = item['title'][0]
            href = item['link'][0]
            url = response.urljoin(href)
            print url.encode('utf8')
            yield item