# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class PunchPipeline:
    def process_item(self, item, spider):
        return item

class SQLlitePipleline(object):
    def open_spider(self, spider):
        self.connection =sqlite3.connect("9JA247_TEST.db")
        self.c = self.connection.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS politics(
             headline TEXT,
             image_url TEXT,
             authour TEXT,
             posted_date TEXT,
             description TEXT,
             newspaper_name TEXT,
             category TEXT,
             url TEXT
            )
        ''')
        self.connection.commit()

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT OR IGNORE INTO politics(headline, image_url, authour, posted_date, description,newspaper_name,category, url) VALUES(?,?,?,?,?,?,?,?)
        
        ''', (  item.get('headline'),
                item.get('image_url'),
                item.get('authour'),
                item.get('posted_date'),
                item.get('description'),
                item.get('newspaper_name'),
                item.get('category'),
                item.get('url')
        ))
        self.connection.commit()
        return item