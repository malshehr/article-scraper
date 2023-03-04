import json
import unittest

from bs4 import BeautifulSoup


def read_html(file):
    with open(file, "r", encoding='utf-8') as f:
        text = f.read()
        return text


def get_article_contents(soup):
    try:
        main_content = soup.find('div', {'id': 'maincontent'}) if soup.find('div', {
            'id': 'maincontent'}) is not None else soup.find('div', {'class': 'content-container'})
        paragraphs = [paragraph.get_text() for paragraph in main_content.find_all('p')]
        article = ' '.join(paragraphs)
        return json.dumps(article)
    except AttributeError:
        return 'N/A'


def get_article_author(soup):
    try:
        if not isinstance(soup.find('a', {'rel': 'author'}), type(None)):
            return soup.find('a', {'rel': 'author'}).getText()
        elif not isinstance(soup.find('address', {'aria-label': 'Contributor info'}), type(None)):
            return soup.find('address', {'aria-label': 'Contributor info'}).getText()
        elif not isinstance(soup.find('meta', {'property': 'article:author'}), type(None)):
            return soup.find('meta', {'property': 'article:author'})['content']
        else:
            return 'N/A'
    except KeyError:
        return 'N/A'


def get_article_title(soup):
    try:
        return soup.find('title').getText().split('|')[0].rstrip()
    except (AttributeError, IndexError):
        return 'N/A'


def get_article_publish_time(soup):
    try:
        return soup.find('meta', {'property': 'article:published_time'})['content']
    except (AttributeError, KeyError, TypeError):
        return 'N/A'


def get_article_url(soup):
    try:
        return soup.find('link', {'rel': 'canonical'}, href=True)['href']
    except (AttributeError, KeyError, TypeError):
        return 'N/A'


class ParseArticles(unittest.TestCase):
    def test_parsing_title(self):
        self.soup = BeautifulSoup(read_html("weather-article.htm"), 'html.parser')
        title = "Weather tracker: winter warmth fuels tornadoes in US south-east"
        self.assertEqual(get_article_title(self.soup), title)

    def test_parsing_author(self):
        self.soup = BeautifulSoup(read_html("weather-article.htm"), 'html.parser')
        self.assertEqual(get_article_author(self.soup), "Trevor Mitchell")

    def test_parsing_url(self):
        self.soup = BeautifulSoup(read_html("weather-article.htm"), 'html.parser')
        link = "https://www.theguardian.com/environment/2023/jan/20/weather-tracker-winter-warmth-fuels-tornadoes-us-south-east"
        self.assertEqual(get_article_url(self.soup), link)

    def test_parsing_publish_time(self):
        self.soup = BeautifulSoup(read_html("weather-article.htm"), 'html.parser')
        publish_time = "2023-01-20T08:43:05.000Z"
        self.assertEqual(get_article_publish_time(self.soup), publish_time)

    def testing_parsing_content(self):
        self.soup = BeautifulSoup(read_html("weather-article.htm"), 'html.parser')

        first_paragraph = '''Although temperatures have plummeted in the UK since last weekend, '''
        '''it has been warmer across the Atlantic in southern parts of the US.'''
        '''Dallas Fort Worth airport broke daily maximum records on consecutive days last week,'''
        '''reaching 29C (85F) on 11 January.'''
        last_paragraph = '''Colder air had a more significant impact in the Rocky Mountains region earlier this week.'''
        ''' A winter storm brought heavy snowfall to Colorado on Tuesday. '''
        '''The storm produced about 23cm (9in) of snow at '''
        '''Denver international airport. Breezy conditions also led to significant drifting '''
        '''as the low pressure system tracked north-east, bringing snowfall to Great Plains states '''
        '''including Nebraska and Iowa.'''

        soup_contents = get_article_contents(self.soup)
        self.assertIn(first_paragraph, soup_contents)
        self.assertIn(last_paragraph, soup_contents)


if __name__ == '__main__':
    unittest.main()
