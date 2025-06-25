import scrapy
from ..items import LianjiaItem

class DynamicSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['sh.lianjia.com']

    def start_requests(self):
        # 区域名列表
        districts = ['jinshan',

                     ]
        page_range={'jinshan':88
                     }
        for district in districts:
            for page in range(1, page_range[district]+1):
                url = f'https://sh.lianjia.com/ershoufang/{district}/pg{page}/'
                yield scrapy.Request(url=url, callback=self.parse, meta={'district': district, 'page': page})

    def parse(self, response):

        for title in response.xpath("//ul[@class='sellListContent']/li[@class='clear LOGCLICKDATA']//div[@class='info clear']"):
            print(title)
            item = LianjiaItem()
            item['name'] = title.xpath("./div[@class='title']/a/text()").extract()  # 爬取课程名称
            item['sum_price'] = title.xpath("./div[@class='priceInfo']/div[@class='totalPrice totalPrice2']//span/text()").getall()  # 爬取总价格
            item['squares'] = title.xpath("./div[3]/div/text()").getall()  # 爬取房屋信息
            item['single_price'] = title.xpath(".//div[@class='priceInfo']/div[@class='unitPrice']//span/text()").extract()  # 提取单价
            print(item)
            yield item

