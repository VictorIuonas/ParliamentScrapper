# -*- coding: utf-8 -*-
import logging

import scrapy

from ParliamentScrapper.items import ParliamentVoteSummaryItem, TranscriptBlock

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
        for sel in response.xpath('//div[@class = "grup-parlamentar-list grupuri-parlamentare-list"]/table/tbody/tr'):
            item = ParliamentVoteSummaryItem()

            item['url_to_vote_details'] = response.urljoin(sel.css('a::attr(href)')[0].extract())
            item['time_of_vote'] = sel.xpath('.//u')[1].extract()
            vote_id_components = sel.xpath('.//u/a/text()').extract()
            item_id = vote_id_components[1]
            if len(vote_id_components) > 2:
                item_id = item_id + ' ' + vote_id_components[2]
            item['id'] = item_id
            item['description'] = sel.xpath('.//td/text()').extract()[4].replace('\n', '')

            url_to_details = response.urljoin(item['url_to_vote_details'])
            request_to_details = scrapy.Request(
                url_to_details, callback=self.parse_details, errback=self.parse_error,
                headers={
                    'Host': 'www.cdep.ro',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
                }
            )
            request_to_details.meta['item'] = item
            yield request_to_details

    def parse_details(self, response):
        logger.info('parsing the details')
        item = response.meta['item']

        selected_main_table = response.css('.program-lucru-detalii')[0]
        row_to_transcript = selected_main_table.xpath('.//table//tr')[2]
        url_to_transcript = response.urljoin(row_to_transcript.css('a::attr(href)')[0].extract())
        item['url_to_transcript'] = url_to_transcript

        logger.info(f'creating req to transcript at: {url_to_transcript}')
        request_to_transcript = scrapy.Request(
            url_to_transcript, callback=self.parse_transcript, errback=self.parse_error,
            headers={
                'Host': 'www.cdep.ro',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
            }
        )

        item['transcript'] = []
        request_to_transcript.meta['item'] = item

        yield request_to_transcript

    def parse_transcript(self, response):
        logger.info('parsing transcript')
        item = response.meta['item']
        transcript = item['transcript']

        selected_main_table = response.css('#olddiv').css('table')[1]

        current_speaker = ''

        all_relevant_tds = selected_main_table.css('td[width="100%"]')
        for relevant_td in all_relevant_tds:
            all_paragraphs = relevant_td.xpath('.//p|.//li')
            current_content = ''

            for paragraph in all_paragraphs:
                speaker_paragraph = paragraph.css('a')

                if speaker_paragraph:
                    current_speaker = speaker_paragraph.css('font::text').get()
                else:
                    paragraph_content = ' '.join(paragraph.css('::text').extract())
                    current_content = f'{current_content}{paragraph_content}'

            transcript_block = TranscriptBlock()
            transcript_block['speaker_name'] = current_speaker
            transcript_block['content'] = ' '.join(current_content.split())
            transcript.append(transcript_block)

        yield item

    def parse_error(self, failure):
        logger.error('got error')
        logger.error(f'failed request to: {failure.value.response.text}')
