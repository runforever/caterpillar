# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import psycopg2
import datetime


class HousePipeline(object):

    def open_spider(self, spider):
        hostname = 'postgres'
        username = 'admin'
        password = 'root'
        database = 'caterpillar'
        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database
        )
        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        now = datetime.datetime.now()
        house_json = json.dumps(dict(item), ensure_ascii=False)

        self.cur.execute(
            "insert into house(house, created_at, updated_at, source_url) values(%s, %s, %s, %s)",
            (house_json, now, now, item['source_url'])
        )
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
