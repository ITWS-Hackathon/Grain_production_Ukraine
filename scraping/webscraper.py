import requests
from lxml import html


class Scraper:
	def __init__(self, url):
		self.url = url
		self.tree = None

	def scrape(self):
    page = requests.get(self.url)
    self.tree = html.fromstring(page.content)

	def process(self,classname,type)
    warnings = (self.tree.xpath('//div[@class="{}}"]/{}}()'))
    

if __name__ == '__main__':
	url = ""