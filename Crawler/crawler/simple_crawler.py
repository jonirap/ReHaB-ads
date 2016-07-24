import re
import socket
import socks
import stem.process
import traceback
from collections import Counter
from html.parser import HTMLParser
from stem.util import term
from urllib import parse
from urllib.request import urlopen

SOCKS_PORT = 7000

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket


def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo


class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    new_url = parse.urljoin(self.base_url, value)
                    self.links = self.links + [new_url]

    def change_url(self, url):
        self.base_url = url
        self.data = urlopen(url).read().decode("utf-8")
        self.links = []

    def parse_page(self):
        self.feed(self.data)


def spider(url, max_pages, tor):
    pages_to_visit = set([url])
    number_visited = 0
    parser = LinkParser()
    while number_visited < max_pages and number_visited < len(pages_to_visit):
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
            tor.kill()
            print("!!fail!!")
            traceback.print_exc()


def print_bootstrap_lines(line):
    # if "Bootstrapped " in line:
        print(term.format(line, term.Color.BLUE))
tor = stem.process.launch_tor_with_config(
    tor_cmd='C:\\Users\\jonir_000\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe',
    config={
        'SocksPort': str(SOCKS_PORT)
        },
    init_msg_handler=print_bootstrap_lines
)
spider("https://www.facebook.com/", 2, tor)
tor.kill()
