# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from ..items import DemoItem
from ..pipelines import DemoPipeline



class ChoubaiSpider(scrapy.Spider):
    name = 'choubai'
    allowed_domains = ['www.cnxox.com']
    start_urls = ['http://www.cnxox.com/']

    def parse(self,  response):
        # print(response.url)
        # 获取页面内容
        # content = str(response.body,encoding="utf-8")
        # print(content)

        # 找到文档中所有的A标签
        # hxs = Selector(response=response).xpath('//a')
        # for i in hxs:
        #     print(i.extract())  #将对象转换为字符串

        # 获取文档中标签对象标题和URL
        hxs1 = Selector(response=response).xpath('//article[@class="excerpt excerpt-one"]')

        for i in hxs1:
            obj = i.xpath('.//h2/a/text()').extract()  #获取标题内容
            name=obj[0]
            href = i.xpath('.//h2/a/@href').extract() #获取URL
            url=href[0]

            item_obj=DemoItem(name=name,url=url)  #封装
            # print(item_obj)
            yield item_obj

        #获取当前页的所有页码
        hxs2 = Selector(response=response).xpath('//div[@class="pagination pagination-multi"]//a[starts-with(@href,"http")]/@href').extract() #获取属性值
        for url in hxs2:
            # 将新要访问的url添加到调度器
             yield Request(
                 url=url,
                 callback=self.parse
             )