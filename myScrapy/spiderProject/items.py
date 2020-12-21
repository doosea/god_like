# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from models.es_types import QsbkTYpe, es


def gen_suggest(index, info_tuple):
    use_word = set()
    suggestion = []
    for text, weight in info_tuple:
        if text:
            # 使用es 的analyze接口分析字符串
            print(text[0])
            print(type(text[0]))
            # words = es.indices.analyze(index=index, params={"filter": ["lowercase"]}, body=text[0])
            words = es.indices.analyze(index=index, body={"text": text[0],  "filter": ["lowercase"]}) # 'analyzer': "ik_max_word",
            analyzed_word = set([word["token"] for word in words["tokens"] if len(word["token"]) >= 1])
            new_words = analyzed_word - use_word
        else:
            new_words = set()

        if new_words:
            suggestion.append({"input": list(new_words), "weight": weight})

    return suggestion


class SpiderprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QsbkItem(scrapy.Item):
    author_name = scrapy.Field()
    author_age = scrapy.Field()
    head_img_url = scrapy.Field()
    content_des = scrapy.Field()
    detail_url = scrapy.Field()
    fav_number = scrapy.Field()
    comment_number = scrapy.Field()
    first_comment = scrapy.Field()

    def save_to_es(self):
        qsbk = QsbkTYpe()
        qsbk.author_age = self["author_age"]
        qsbk.author_name = self["author_name"]
        qsbk.author_age = self["author_age"]
        qsbk.head_img_url = self["head_img_url"]
        qsbk.detail_url = self["detail_url"]
        qsbk.content_des = self["content_des"]
        qsbk.fav_number = self["fav_number"]
        qsbk.comment_number = self["comment_number"]
        qsbk.first_comment = self["first_comment"]

        qsbk.suggest = gen_suggest(QsbkTYpe._index._name, ((qsbk.content_des, 10), (qsbk.first_comment, 7)))

        qsbk.save()

        return
