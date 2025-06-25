# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    name = scrapy.Field()#房子名称
    sum_price = scrapy.Field()#房子总价
    squares = scrapy.Field()#房子面积
    single_price = scrapy.Field()#房子每平方米单价
    pass
