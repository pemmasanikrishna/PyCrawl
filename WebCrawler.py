from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


class Parser(HTMLParser):

    def handle_starttag(self, tag, attributes):
        if tag == 'a':
            for (key, value) in attributes:
                if key == 'href' and value not in ['/', '', ' ', '#'] and value[-1] not in[';', ':']:
                    new_url = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [new_url]
                    break

    def getlinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        if response.getheader('Content-Type').index('text/html') != -1:
            htmlbytes = response.read()
            htmlcontent = htmlbytes.decode("utf-8")
            self.feed(htmlcontent)
            return htmlcontent, self.links
        else:
            return "", []

"""This method is used for crawling the given web link
    Usage:
    This takes 2 params @url,@max_pages
    url is the web link that is to be crawled.
    max_pages is the depth of crawling i.e the number of links to be crawled.
"""
def crawl(url, max_pages=20):
    pages_to_visit = [url]
    visited_number = 1
    urls_visited = {}
    while visited_number <= max_pages and pages_to_visit != []:
        url = pages_to_visit.pop(0)
        if url not in urls_visited and url.startswith("http://"):
            urls_visited[url] = url

            try:
                print(visited_number, "Visiting:", url)
                parser = Parser()
                data, links = parser.getlinks(url)
                print('Urls found in the above link:',len(links))
                pages_to_visit.extend(links)
                print('Total Urls Left for crawling:',len(pages_to_visit))
                visited_number += 1

            except:
                print("Failed to fetch the link")



crawl("http://python.org/")