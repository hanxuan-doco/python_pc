


class DemoPipeline(object):

    def open_spider(self, spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        self.f = open("E:\pycharm\.idea\Crawler\demo\\new.json", 'a')

    def close_spider(self, spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        self.f.close()

    def process_item(self, item, spider):
        """
        每当数据需要持久化时，就会被调用
        :param item:
        :param spider:
        :return:
        """
        # if spider.name == 'choubai '
        tpl = "%s\n%s\n\n" % (item['name'], item['url'])
        self.f.write(tpl)
        # 交给下一个pipeline处理
        # return item
        # 丢弃item，不交给
        # raise DropItem()


class Demo1Pipeline(object):

    def __init__(self, conn_str):
        self.conn_str = conn_str

    @classmethod
    def from_crawler(cls, crawler):
        """
        初始化时候，用于创建pipeline对象
        :param crawler:
        :return:
        """
        conn_str = crawler.settings.get('DB')
        return cls(conn_str)

    def open_spider(self, spider):
        """
        爬虫开始执行时，调用
        :param spider:
        :return:
        """
        self.conn = open(self.conn_str, 'a')

    def close_spider(self, spider):
        """
        爬虫关闭时，被调用
        :param spider:
        :return:
        """
        self.conn.close()

    def process_item(self, item, spider):
        """
        每当数据需要持久化时，就会被调用
        :param item:
        :param spider:
        :return:
        """
        # if spider.name == 'choubai '
        tpl = "%s\n%s\n\n" % (item['title'], item['href'])
        self.conn.write(tpl)
