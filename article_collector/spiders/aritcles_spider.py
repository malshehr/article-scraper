from web_parser.guardian_parser import GuardianParser
from bs4 import BeautifulSoup
from article_collector.items import ArticleCollectorItem
import scrapy


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ['theguardian.com']

    # default url for scrapy crawlers: fetches all articles on international page,
    # parses the links, then parses every article individually
    def start_requests(self):
        urls = [
            'https://www.theguardian.com/international',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(response.body, 'html.parser')
        website = soup.findAll('a', {"class": 'js-headline-text'}, href=True)
        articles_links = [link['href'] for link in website]
        for link in articles_links:
            yield scrapy.Request(link, callback=self.parse_articles)

    # guardian article parser: uses GuardianParser object to parse
    # a given response from the guardian news website
    def parse_articles(self, response):
        guardian_parser = GuardianParser(response)
        article_item = ArticleCollectorItem()
        article_item['title'] = guardian_parser.retrieve_title()
        article_item['author'] = guardian_parser.retrieve_author()
        article_item['url'] = guardian_parser.retrieve_url()
        article_item['content'] = guardian_parser.retrieve_text()
        article_item['length'] = len(article_item['content'])
        article_item['publish_date'] = guardian_parser.retrieve_published_time()
        return article_item
