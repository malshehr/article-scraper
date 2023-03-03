import json

from bs4 import BeautifulSoup


class GuardianParser:
    def __init__(self, response):
        self.soup = BeautifulSoup(response.body, 'html.parser')

    def retrieve_title(self):
        try:
            return self.soup.find('title').getText().split('|')[0].rstrip()
        except (AttributeError, IndexError):
            return 'N/A'

    def retrieve_text(self):
        try:
            main_content = self.soup.find('div', {'id': 'maincontent'}) if self.soup.find('div', {
                'id': 'maincontent'}) is not None else self.soup.find('div', {'class': 'content-container'})
            links = [e.get_text() for e in main_content.find_all('p')]
            article = '\n'.join(links)
            return json.dumps(article)
        except AttributeError:
            return 'N/A'

    def retrieve_author(self):
        try:
            if not isinstance(self.soup.find('a', {'rel': 'author'}), type(None)):
                return self.soup.find('a', {'rel': 'author'}).getText()
            elif not isinstance(self.soup.find('address', {'aria-label': 'Contributor info'}), type(None)):
                return self.soup.find('address', {'aria-label': 'Contributor info'}).getText()
            elif not isinstance(self.soup.find('meta', {'property': 'article:author'}), type(None)):
                return self.soup.find('meta', {'property': 'article:author'})['content']
            else:
                return 'N/A'
        except KeyError:
            return 'N/A'

    def retrieve_url(self):
        try:
            return self.soup.find('link', {'rel': 'canonical'}, href=True)['href']
        except (AttributeError, KeyError, TypeError):
            return 'N/A'

    def retrieve_published_time(self):
        try:
            return self.soup.find('meta', {'property': 'article:published_time'})['content']
        except (AttributeError, KeyError, TypeError):
            return 'N/A'
