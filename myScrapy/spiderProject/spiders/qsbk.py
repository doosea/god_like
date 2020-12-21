import scrapy
from scrapy.http import Request
from ..items import QsbkItem

class QsbkSpider(scrapy.Spider):
    name = 'qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['http://qiushibaike.com/text/']

    def parse(self, response):
        qb_item = QsbkItem()
        selectors = response.xpath('//*[@id="content"]/div/div[2]/div')
        for selector in selectors:
            author_name = selector.xpath('./div[1]/a[2]/h2/text()').get().strip()
            author_age = selector.xpath('./div[1]/div/text()').get()
            head_img_url = selector.xpath('./div[1]/a[1]/img/@src').get().replace("//", "")
            # 内容不全, 含有 <br> 的之后拿不到...
            content_des = selector.xpath('./a/div/span/text()').get().strip()
            detail_url = response.urljoin(selector.xpath('./a/@href').get())
            fav_number = selector.xpath('./div[2]/span[1]/i/text()').get()
            comment_number = selector.xpath('./div[2]/span[2]/a/i/text()').get()
            first_comment = selector.xpath('./a[2]/div/div/text()').get()

            try:
                author_age = int(author_age)
                fav_number = int(fav_number)
                comment_number = int(comment_number)
            except Exception as e:
                print(e)

            res = {
                "author_name": author_name,
                "author_age": author_age,
                "head_img_url": head_img_url,
                "content_des": content_des,
                "detail_url": detail_url,
                "fav_number": fav_number,
                "comment_number": comment_number,
                "first_comment": first_comment
            }
            print(res)
            qb_item["author_name"] = author_name,
            qb_item["author_age"] = author_age,
            qb_item["head_img_url"] = head_img_url,
            qb_item["detail_url"] = detail_url,
            qb_item["content_des"] = content_des,
            qb_item["fav_number"] = fav_number,
            qb_item["comment_number"] = comment_number,
            qb_item["first_comment"] = first_comment,

            yield qb_item

        next_url = response.xpath('//ul[@class="pagination"]/li[last()]/a/@href').get()
        if next_url:
            yield Request(url=response.urljoin(next_url), callback=self.parse)
