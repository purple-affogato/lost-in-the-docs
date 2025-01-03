import scrapy
from scrapy.crawler import CrawlerProcess

class PythonDocsSpider(scrapy.Spider):
    name = "python_docs"
    start_urls = ["https://docs.python.org/3/library/index.html",
                  "https://docs.python.org/3/reference/index.html",
                  "https://docs.python.org/3/using/index.html",
                  "https://docs.python.org/3/howto/index.html",
                  "https://docs.python.org/3/tutorial/index.html",
                  ]

    def parse(self, response):
        tabs = response.css("li.toctree-l1, li.toctree-l2")