# -*- coding: utf-8 -*-

"""
@Time        : 2020/12/20
@Author      : dosea
@File        : es_types
@Description :  使用elasticsearch_dsl 连接本地es库,建立索引类型
"""
from elasticsearch_dsl import Document, Completion, Text, Integer, Keyword
from elasticsearch_dsl import connections

es = connections.create_connection(hosts=['localhost'], timeout=20)


class QsbkTYpe(Document):
    # author_name = Text(analyzer='ik__max_word')
    suggest = Completion()
    author_name = Text()
    author_age = Integer()
    head_img_url = Keyword()
    content_des = Text()
    detail_url = Keyword()
    fav_number = Integer()
    # comment_number = Integer(analyzer='ik__max_word')
    # first_comment = Text(analyzer='ik__max_word')
    comment_number = Integer()
    first_comment = Text()

    class Index:
        name = 'qsbk'

    # 下面这种写法是过时的
    # class Meta:
    #     index = 'qsbk'


if __name__ == '__main__':
    # 注意这里类型后面没有()
    QsbkTYpe.init()
