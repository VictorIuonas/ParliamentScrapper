import os
from typing import List
from unittest.mock import MagicMock

import scrapy

from items import ParliamentVoteSummaryItem
from spiders.SpiderCDEP import SpidercdepSpider
from tests.test_lib.resources_lib import fake_response_from_file


class TestSpiderCDEP:

    def test_parse_summary(self):
        expected_detailed_vote_info_requests = [
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23134&idl=1',
            },
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23135&idl=1',
            },
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23136&idl=1',
            },
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23137&idl=1',
            }
        ]

        scenario = self._Scenario()

        scenario.given_a_request_for_a_vote_summary_page(os.path.join('SpiderCDEP', 'votes_summary.html'))

        scenario.when_sending_the_get_summary_request()

        scenario.then_the_request_data_will_match([MagicMock()])

        scenario.when_parsing_the_page_summary_response()

        scenario.then_the_parse_vote_summary_will_generate_the_requests_for_the_vote_details(
            expected_detailed_vote_info_requests
        )

    def test_parse_vote_details(self):
        preset_item = ParliamentVoteSummaryItem()
        preset_item['url_to_vote_details'] = 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23134&idl=1'

        expected_detailed_vote_info_requests = [
            {
                'url_to_vote_details': 'http://www.cdep.ro/pls/steno/evot2015.nominal?idv=23134&idl=1',
                'url_to_transcript': 'http://www.cdep.ro/pls/steno/steno2015.stenograma?ids=8132&idm=5'
            }
        ]

        scenario = self._Scenario()

        scenario.given_a_request_for_a_vote_details(os.path.join('SpiderCDEP', 'vote_details.html'), preset_item)

        scenario.when_parsing_the_vote_details_response()

        scenario.then_the_parse_vote_details_will_generate_the_requests_for_the_vote_transcript(
            expected_detailed_vote_info_requests
        )

    class _Scenario:

        def __init__(self):
            self.target = SpidercdepSpider(date='20200203')
            self.actual_summary_requests = None
            self.actual_summary_parse_result = None
            self.actual_summary_parse_details_result = None

            self.response_get_summary = ''
            self.response_get_vote_details = ''

        def given_a_request_for_a_vote_summary_page(self, path_to_response_body: str):
            self.response_get_summary = fake_response_from_file(path_to_response_body)

        def given_a_request_for_a_vote_details(
                self, path_to_response_body: str, preset_item: ParliamentVoteSummaryItem
        ):
            self.response_get_vote_details = fake_response_from_file(path_to_response_body)
            self.response_get_vote_details.meta['item'] = preset_item

        def when_sending_the_get_summary_request(self):
            self.actual_summary_requests = self.target.start_requests()

        def when_parsing_the_page_summary_response(self):
            self.actual_summary_parse_result = list(self.target.parse_summary(self.response_get_summary))

        def when_parsing_the_vote_details_response(self):
            self.actual_summary_parse_details_result = list(self.target.parse_details(self.response_get_vote_details))

        def then_the_request_data_will_match(self, expected_requests: List[scrapy.Request]):
            assert len(self.actual_summary_requests) == len(expected_requests)

        def then_the_parse_vote_summary_will_generate_the_requests_for_the_vote_details(
                self, expected_parse_results: List
        ):
            assert len(expected_parse_results) == len(self.actual_summary_parse_result)
            for expected_req, actual_req in zip(expected_parse_results, self.actual_summary_parse_result):
                actual_item = actual_req.meta['item']
                assert expected_req['url_to_vote_details'] == actual_item['url_to_vote_details']

        def then_the_parse_vote_details_will_generate_the_requests_for_the_vote_transcript(
                self, expected_parse_result: List
        ):
            assert len(expected_parse_result) == len(self.actual_summary_parse_details_result)
            for expected_req, actual_req in zip(expected_parse_result, self.actual_summary_parse_details_result):
                actual_item = actual_req.meta['item']

                assert expected_req['url_to_vote_details'] == actual_item['url_to_vote_details']
                assert expected_req['url_to_transcript'] == actual_item['url_to_transcript']
