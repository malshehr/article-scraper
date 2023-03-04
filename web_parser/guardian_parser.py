import json
from bs4 import BeautifulSoup

# GuardianParser class: Responsible for parsing relevant components of a guardian article


class GuardianParser:
    def __init__(self, response):

        # obtaining BeautifulSoup object that helps query tags in the response body
        self.soup = BeautifulSoup(response.body, 'html.parser')

    def retrieve_title(self):
        # Removing irrelevant part of title tag e.g:
        # UK now seen as ‘toxic’ for satellite launches, MPs told | Space | The Guardian
        try:
            return self.soup.find('title').getText().split('|')[0].rstrip()
        except (AttributeError, IndexError):
            return 'N/A'

    def retrieve_text(self):
        # Retrieving the paragraph html tags that persist in the content div tag
        # then joining them together
        try:
            main_content = self.soup.find('div', {'id': 'maincontent'}) if self.soup.find('div', {
                'id': 'maincontent'}) is not None else self.soup.find('div', {'class': 'content-container'})
            paragraphs = [paragraph.get_text() for paragraph in main_content.find_all('p')]
            article = '\n'.join(paragraphs)
            return json.dumps(article)
        except AttributeError:
            return 'N/A'

    def retrieve_author(self):
        # Retrieving the author while considering the inconsistencies encountered within
        # guardian articles
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
