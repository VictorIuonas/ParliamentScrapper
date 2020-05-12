# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParliamentscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ParliamentVoteSummaryItem(scrapy.Item):
    id = scrapy.Field()
    time_of_vote = scrapy.Field()
    url_to_vote_details = scrapy.Field()
    url_to_transcript = scrapy.Field()
    description = scrapy.Field()
    no_of_people_present = scrapy.Field()
    no_of_votes_for = scrapy.Field()
    no_of_votes_against = scrapy.Field()
    no_of_abstentions = scrapy.Field()
    no_of_no_votes = scrapy.Field()
