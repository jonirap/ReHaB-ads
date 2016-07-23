from urllib import parse
from collections import Counter
import re
from html.parser import HTMLParser
from urllib.request import urlopen


class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    new_url = parse.urljoin(self.base_url, value)
                    self.links = self.links + [new_url]

    def change_url(self, url):
        self.base_url = url
        response = urlopen(url)
        self.data = response.read().decode("utf-8")
        self.links = []

    def parse_page(self):
        self.feed(self.data)


def spider(url, max_pages):
    pages_to_visit = set([url])
    number_visited = 0
    parser = LinkParser()
    while number_visited < max_pages and pages_to_visit != []:
        url = list(pages_to_visit)
        url = url[number_visited]
        number_visited += 1
        print(number_visited, "Visiting:", url)
        try:
            parser.change_url(url)
            parser.parse_page()
            pages_to_visit |= set(parser.links)
            words = re.findall(r'\w+', parser.data.lower())
            print(Counter(words).most_common(10))
        except:
            print("!!fail!!")

spider("https://www.facebook.com/", 30)
