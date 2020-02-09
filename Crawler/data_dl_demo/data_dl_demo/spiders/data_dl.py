# -*- coding: utf-8 -*-
import scrapy
import time
import re
class GithubSpider(scrapy.Spider):
    name = 'data_dl'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/login']

    def parse(self, response):
        authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
        utf8 = response.xpath("//input[@name='utf8']/@value").extract_first()
        commit = response.xpath("//input[@name='commit']/@value").extract_first()
        print(authenticity_token)
        print(utf8)
        print(commit)
        post_data = dict(
            login="1009070053@qq.com",
            password="15930057505han",
            authenticity_token=authenticity_token,
            commit=commit
        )
        yield scrapy.FormRequest(
            "https://github.com/session",
            formdata=post_data,
            callback=self.after_login
        )

    def after_login(self,response):
        # print(response)
        print(response.text)