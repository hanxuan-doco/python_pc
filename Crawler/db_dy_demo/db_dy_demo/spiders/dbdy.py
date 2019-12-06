# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import json
from ..items import DbDyDemoItem
from ..pipelines import DbDyDemoPipeline
import time


class DbdySpider(scrapy.Spider):
    name = 'dbdy'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=0&genres=%E5%8A%A8%E7%94%BB']
                 # https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=20&genres=%E5%8A%A8%E7%94%BB
                 # https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start=40&genres=%E5%8A%A8%E7%94%BB
    st = 0

    def parse(self, response):
        a = json.loads(response.body,encoding="utf-8").values()
        for i in a:
            for j in i:
                """

                {'directors': ['宫崎骏'], 'rate': '9.3', 'cover_x': 1080, 'star': '45', 'title': '千与千寻', 'url': 'https://movie.douban.com/subject/1291561/', 'casts': ['柊瑠美', '入野自由', '夏木真理', '菅原文太', '中村彰男'], 'cover': 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2557573348.jpg', 'id': '1291561', 'cover_y': 1560}

                directors
                rate
                cover_x
                star
                title
                url
                casts
                cover
                id
                cover_y
                """
                item_obj = DbDyDemoItem(
                    directors = j.get('directors'),
                    rate = j.get('rate'),
                    cover_x = j.get('cover_x'),
                    star = j.get('star'),
                    title = j.get('title'),
                    url = j.get('url'),
                    casts = j.get('casts'),
                    cover = j.get('cover'),
                    id = j.get('id'),
                    cover_y = j.get('cover_y'),
                )
                # print(item_obj)
                yield item_obj

        url = response.url
        ym = int(url[77:-26])+20
        url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=&start="+str(ym)+"&genres=%E5%8A%A8%E7%94%BB"
        time.sleep(5)
        yield Request(url=url,callback=self.parse)