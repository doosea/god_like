# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb


class SpiderprojectPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipline:
    def __init__(self):
        self.conn = MySQLdb.connect("localhost", "root", "Dosea0118", "es", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = """
        insert into qiushibaike(author_name, author_age, head_img_url, content_des, detail_url,fav_number, comment_number,first_comment)
        VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(sql, (item["author_name"],
                                  item["author_age"],
                                  item["head_img_url"],
                                  item["content_des"],
                                  item["detail_url"],
                                  item["fav_number"],
                                  item["comment_number"],
                                  item["first_comment"])
                            )
        self.conn.commit()
        return item


class ElasticsearchPipline:
    def process_item(self, item, spider):
        item.save_to_es()
        return item
