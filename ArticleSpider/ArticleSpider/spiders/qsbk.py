import scrapy
import pprint

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
