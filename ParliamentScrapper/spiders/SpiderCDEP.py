# -*- coding: utf-8 -*-
import logging

import scrapy

from ParliamentScrapper.items import ParliamentVoteSummaryItem

logger = logging.getLogger()


class SpidercdepSpider(scrapy.Spider):
    name = 'SpiderCDEP'
    allowed_domains = ['cdep.ro']

    def __init__(self, date: str, *args, **kwargs):
        super(SpidercdepSpider, self).__init__(*args, **kwargs)
        self.date = date
        self.start_urls = [f'http://www.cdep.ro/pls/steno/evot2015.data?dat={date}']

    def start_requests(self):
        # create a get request with error handling to see why we get 500 status code
        logger.info('started the request')
        return [
            scrapy.Request(
                self.start_urls[0], callback=self.parse_summary, errback=self.parse_error,
                headers={
                    'Host': 'www.cdep.ro',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
                }
            )
        ]

    def parse_summary(self, response):
        logger.info('parsing the summary')
        for sel in response.xpath('//div[@class = "grup-parlamentar-list grupuri-parlamentare-list"]/table/tbody/tr/td'):
            item = ParliamentVoteSummaryItem()
            item['time_of_vote'] = sel.xpath('/a/u/text()').extract()
            yield item

    def parse_error(self, failure):
        logger.error('got error')
        logger.error(f'failed request to: {failure.value.response.text}')
