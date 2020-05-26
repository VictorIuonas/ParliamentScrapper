# -*- coding: utf-8 -*-
import logging
from typing import List

import scrapy
from scrapy import Selector

from ParliamentScrapper.items import ParliamentVoteSummaryItem, TranscriptBlock, VoteItem

logger = logging.getLogger(__file__)


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
        for table_row in response.xpath(
                '//div[@class = "grup-parlamentar-list grupuri-parlamentare-list"]/table/tbody/tr[@bgcolor="#ffffff"]'
        ):
            item = ParliamentVoteSummaryItem()

            link_selector = table_row.css('a::attr(href)')
            is_link_to_details_present = len(link_selector) != 0
            if is_link_to_details_present:
                item['url_to_vote_details'] = response.urljoin(link_selector[0].extract())

            all_row_data = table_row.css('td')

            time_of_vote_cell = all_row_data[1]
            vote_id_cell = all_row_data[2]
            vote_description_cell = all_row_data[3]

            item['time_of_vote'] = self._extract_time_of_vote(time_of_vote_cell).replace('\n', '')
            item['id'] = self._extract_vote_id(vote_id_cell).replace('\n', '')
            item['description'] = self._extract_content_selector_from_optional_link_cell(
                vote_description_cell
            ).get().replace('\n', '')

            if is_link_to_details_present:
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
            else:
                yield item

    @classmethod
    def _extract_content_selector_from_optional_link_cell(cls, cell: Selector) -> Selector:
        content_in_link = cell.css('a::text')
        if content_in_link:
            return content_in_link

        return cell.css('::text')

    @classmethod
    def _extract_time_of_vote(cls, time_of_vote_cell: Selector) -> str:
        return cls._extract_content_selector_from_optional_link_cell(time_of_vote_cell).get()

    @classmethod
    def _extract_vote_id(cls, vote_id_cell: Selector) -> str:
        id_list_selector = cls._extract_content_selector_from_optional_link_cell(vote_id_cell)
        item_id = ' '.join(id_list_selector.extract())

        return item_id

    def parse_details(self, response):
        logger.info('parsing the details')
        item = response.meta['item']

        item['all_votes'] = self._extract_all_votes(response)

        selected_main_table = response.css('.program-lucru-detalii')[0]
        header_table = selected_main_table.xpath('.//table')[0]
        main_table_rows = header_table.xpath('.//tr')

        is_link_to_transcript_present = len(main_table_rows) > 2
        if is_link_to_transcript_present:
            row_with_link = main_table_rows[2]
            item['url_to_transcript'] = response.urljoin(row_with_link.css('a::attr(href)')[0].extract())
        else:
            item['url_to_transcript'] = 'not available'

        if is_link_to_transcript_present:
            logger.info(f'creating req to transcript at: {item["url_to_transcript"]}')
            request_to_transcript = scrapy.Request(
                item['url_to_transcript'], callback=self.parse_transcript, errback=self.parse_error,
                headers={
                    'Host': 'www.cdep.ro',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0'
                }
            )

            item['transcript'] = []
            request_to_transcript.meta['item'] = item

            yield request_to_transcript
        else:
            yield item

    @classmethod
    def _extract_all_votes(cls, response) -> List[VoteItem]:
        result = []
        vote_table = response.css('table[width="100%"][cellspacing="0"][cellpadding="3"]')
        if len(vote_table) > 0:
            last_table_index = len(vote_table) - 1
            vote_rows = vote_table[last_table_index].xpath(".//tr[@valign='top']")
            for row in vote_rows:
                vote_cells = row.xpath('.//td')
                is_member_role_present = len(vote_cells) > 4

                member_role = ''
                vote_value_index = 3
                group_value_index = 2

                if is_member_role_present:
                    vote_value_index = 4
                    group_value_index = 3
                    member_role = vote_cells[2].css('::text').get()

                single_result = VoteItem()
                single_result['name_and_surname'] = vote_cells[1].css('::text').get()
                single_result['role'] = member_role
                single_result['group_membership'] = vote_cells[group_value_index].css('::text').get()
                vote_value = vote_cells[vote_value_index].css('::text').get()
                single_result['vote_value'] = vote_value.replace('\n', '')

                result.append(single_result)

        return result

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
