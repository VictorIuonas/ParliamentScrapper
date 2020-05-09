from typing import List
from unittest.mock import MagicMock

import scrapy

from spiders.SpiderCDEP import SpidercdepSpider


class TestSpiderCDEP:

    def test_parse_summary(self):
        scenario = self._Scenario()

        scenario.when_sending_the_get_summary_request()

        scenario.then_the_request_data_will_match([MagicMock()])

    class _Scenario:

        def __init__(self):
            self.target = SpidercdepSpider(date='20200203')
            self.actual_summary_requests = None

        def when_sending_the_get_summary_request(self):
            self.actual_summary_requests = self.target.start_requests()

        def then_the_request_data_will_match(self, expected_requests: List[scrapy.Request]):
            assert len(self.actual_summary_requests) == len(expected_requests)
