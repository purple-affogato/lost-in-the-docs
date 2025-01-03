import json
import scrapy
from scrapy.crawler import CrawlerProcess

keywords = ["poop"]

class PandasSpider(scrapy.Spider):
    name = "pandas"
    start_urls = [
        "https://pandas.pydata.org/docs/reference/index.html",
        "https://pandas.pydata.org/docs/reference/io.html",
        "https://pandas.pydata.org/docs/reference/general_functions.html",
        "https://pandas.pydata.org/docs/reference/series.html",
        "https://pandas.pydata.org/docs/reference/frame.html",
        "https://pandas.pydata.org/docs/reference/arrays.html",
        "https://pandas.pydata.org/docs/reference/indexing.html",
        "https://pandas.pydata.org/docs/reference/offset_frequency.html",
        "https://pandas.pydata.org/docs/reference/window.html",
        "https://pandas.pydata.org/docs/reference/groupby.html",
        "https://pandas.pydata.org/docs/reference/resampling.html",
        "https://pandas.pydata.org/docs/reference/style.html",
        "https://pandas.pydata.org/docs/reference/plotting.html",
        "https://pandas.pydata.org/docs/reference/options.html",
        "https://pandas.pydata.org/docs/reference/extensions.html",
        "https://pandas.pydata.org/docs/reference/testing.html",
        "https://pandas.pydata.org/docs/reference/missing_value.html"
    ]

    def parse(self, response):
        rows = response.css('tr.row-odd, tr.row-even')
        for t in rows:
            link = t.css('a.reference.internal')
            title = link.css('span.pre::text').get()
            if title is None:
                continue
            score = self._get_match_score(title)
            if score > 0:
                yield {'title': title,
                        'link': link.attrib['href'],
                        'score': score}

        

    def _get_match_score(self, title: str) -> int:
        cnt = 0
        for k in keywords:
            if k not in title.casefold():
                return 0
            cnt += len(k)
        return cnt / len(title)


def crawl_process():
    base_url = "https://pandas.pydata.org/docs/reference/"
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "pandas_data.json": {
                    "format": "json",
                    "overwrite": "True"
                }
            },
            "LOG_FILE": "pandas_spider.log"
        }
    )

    process.crawl(PandasSpider)
    process.start()  # the script will block here until the crawling is finished
    with open('pandas_data.json', 'r') as f:
        data = json.load(f)
    if len(data) == 0:
        print("Nothing found.")
        return
    data = sorted(data, key=lambda d : d['score'], reverse=True)
    ctr = 0
    print("URLS:")
    for d in data:
        if ctr > 5:
            break
        print(base_url + d['link'])
        ctr += 1