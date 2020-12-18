import scrapy
from scrapy.http import Request


class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['http://qiushibaike.com/']

    def parse(self, response):
        selectors = response.xpath('//*[@class="recommend-article"]/ul/li')
        for selector in selectors:
            ha_number = selector.xpath('./div/div/div/span[1]/text()')
            comment_number = selector.xpath('./div/div/div/span[4]/text()').get()
            title = selector.xpath('./div/a/text()').get()
            author = selector.xpath('./div/div/a/span/text()').get()
            author_head_img = selector.xpath('./div/div/a/img/@src').get().replace("//", "")
            # 链接全路径url
            url = response.urljoin(selector.xpath('./div/a/@href').get())
            res_item = {
                "ha_number": ha_number,
                "comment_number": comment_number,
                "title": title,
                "author": author,
                "author_head_img": author_head_img,
                "url": url,
            }
            print(res_item)
        next_page_url = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').get()
        if next_page_url and "hot" not in next_page_url:
            print("下页网址：", response.urljoin(next_page_url))
            yield Request(url=response.urljoin(next_page_url), callback=self.parse)

    def parse_detail(self, response):
        '''
            提取文章的具体字段的逻辑
        :param response:
        :return:
        '''
        print("进入parse_detail函数")
        selectors = response.xpath('//*[@class="recommend-article"]/ul/li')
        for selector in selectors:
            ha_number = selector.xpath('./div/div/div/span[1]/text()').get()
            comment_number = selector.xpath('./div/div/div/span[4]/text()').get()
            title = selector.xpath('./div/a/text()').get()
            author = selector.xpath('./div/div/a/span/text()').get()
            author_head_img = selector.xpath('./div/div/a/img/@src').get().replace("//", "")
            # 链接全路径url
            url = response.urljoin(selector.xpath('./div/a/@href').get())
            res_item = {
                "ha_number": ha_number,
                "comment_number": comment_number,
                "title": title,
                "author": author,
                "author_head_img": author_head_img,
                "url": url,
            }
            print(res_item)
