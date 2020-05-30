import logging

import scrapy

from items import SpanishDailyPublications

logger = logging.getLogger(__file__)


class CongresoESSpider(scrapy.Spider):
    name = 'CongresoESSpider'
    allowed_domains = ['congreso.es']

    def __init__(self):
        self.start_urls = ['http://www.congreso.es/portal/page/portal/Congreso/Congreso/Publicaciones/PubliOfiUltDias']

    def start_requests(self):
        logger.info('starting request')

        return [
            scrapy.Request(
                self.start_urls[0], callback=self.parse_publications_page, errback=self.parse_error,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
                }
            )
        ]

    def parse_publications_page(self, response):
        item = SpanishDailyPublications()
        url_to_prev_page = ''

        selector_for_link_to_previous_page = response.xpath('//div[@id="fechas"]/ul/li/a')
        if len(selector_for_link_to_previous_page) > 1:
            part_url = selector_for_link_to_previous_page[1].css('::attr(href)')[0].extract()
            url_to_prev_page = response.urljoin(part_url)

        item['link_to_publications'] = []
        selector_for_all_attachments_containers = response.css('li.texto_sesion')
        for container in selector_for_all_attachments_containers:
            paragraph_tag = container.css('a::text').get()
            if paragraph_tag.startswith('Núm'):
                link_to_publication = response.urljoin(container.css('a::attr(href)').extract()[0])
                item['link_to_publications'].append(link_to_publication)

        if url_to_prev_page:
            print('something')
            yield scrapy.Request(
                url_to_prev_page, callback=self.parse_publications_page, errback=self.parse_error,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
                }
            )
        yield item

    def parse_error(self, failure):
        logger.error('got error')
        logger.error(f'failed request to: {failure.value.response.text}')
