# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from pymongo import MongoClient

import settings

logger = logging.getLogger(__file__)


class MongoPipeline:

    def __init__(self):
        self.connection = MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        self.db = self.connection[settings.MONGODB_DB]
        self.collection = self.db[settings.MONGODB_COLLECTION]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item


class ParliamentscrapperPipeline:
    def process_item(self, item, spider):

        return item
