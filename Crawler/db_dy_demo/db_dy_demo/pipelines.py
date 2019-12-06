# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DbDyDemoPipeline(object):
    def open_spider(self, spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        print("开始")
        self.f = open("E:\pycharm\.idea\Crawler\db_dy_demo\dbdy.json", 'a')

    def close_spider(self, spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        print("结束")
        self.f.close()

    def process_item(self, item, spider):
        """
        每当数据需要持久化时，就会被调用
        :param item:
        :param spider:
        :return:
        """
        tpl = "电影名称：%s\n导演：%s\n主演：%s\n评分：%s\nURL：%s\n封面URL：%s\nID号：%s\n\n" % (item['title'],item['directors'],item['casts'],item['rate'],item['url'],item['cover'],item['id'])
        print("--------------")
        print(tpl)
        self.f.write(tpl)
        # 交给下一个pipeline处理
        # return item
        # 丢弃item，不交给
        # raise DropItem()
