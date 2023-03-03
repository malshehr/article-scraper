import scrapy


class ArticleCollectorItem(scrapy.Item):
    url = scrapy.Field()
    source = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    length = scrapy.Field()
    publish_date = scrapy.Field()
    pass

