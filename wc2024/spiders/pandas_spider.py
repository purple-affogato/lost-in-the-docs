import scrapy

class PandasSpider(scrapy.Spider):
    name = "pandas"
    start_urls = [
        "https://pandas.pydata.org/docs/reference/index.html"
    ]

    def __init__(self, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.key_index = 0

    def parse(self, response):
        keywords = ["dataframe", "columns"]
        tabs = response.css('li.toctree-l'+str(self.key_index+1))
        next_page = None
        for t in tabs:
            if keywords[self.key_index].casefold() in t.css('a.reference.internal::text').get().casefold():
                if self.key_index < len(keywords)-1:
                    next_page = t.css('a.reference.internal').attrib['href']
                    self.key_index += 1
                    break
                yield {'match': t.css('a.reference.internal::text').get(),
                       'link': t.css('a.reference.internal').attrib['href']}
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
            