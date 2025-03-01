import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
import json

keywords = ["and", "or"]

class PythonDocsSpider(scrapy.Spider):
    name = "python_docs"
    start_urls = ["https://docs.python.org/3/library/index.html",
                  "https://docs.python.org/3/reference/index.html",
                  "https://docs.python.org/3/using/index.html",
                  "https://docs.python.org/3/howto/index.html",
                  "https://docs.python.org/3/tutorial/index.html",
                  ]
    le1 = LinkExtractor(allow="https://docs.python.org/3", restrict_css='li.toctree-l1', deny='#')

    # only parses start urls
    def parse(self, response):
        links = self.le1.extract_links(response)
        for l in links:
             yield response.follow(l, self.parse_sig)
        # sections = response.css('li')
        # for s in sections:
        #     l = s.css('a.reference.internal::attr(href)').get()
        #     title = "".join(s.css('a.reference.internal::text').getall())
        #     title = title.join(s.css('a+span::text, code+span::text').getall())
        #     if title is None:
        #         continue
        #     print(title)
        #     score = self._get_match_score(title)
        #     if score > 0:      
        #         yield {
        #             "link":l,
        #             "title": title,
        #             "score": score
        #         }
    
    # parses through classes, functions, types, etc.
    def parse_sig(self, response):
        sigs = response.css("dt.sig.sig-object.py")
        for s in sigs:
            link = s.css("a.headerlink::attr(href)").get()
            title = s.css('dt::attr(id)').get()
            if title is None:
                continue
            score = self._get_match_score(title)
            if score > 0:
                yield {
                    "link": response.request.url + link,
                    "title": title,
                    "score": score
                }

            
    def _get_match_score(self, title: str) -> int:
        cnt = 0
        for k in keywords:
            if k.casefold() not in title.casefold():
                return 0
            cnt += len(k)
        return cnt / len(title)

    def _get_section_title(self, section) -> str:
        pass
        

def crawl_process():
    data_file = "python_docs_data.json"
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                data_file: {
                    "format": "json",
                    "overwrite": "True"
                }
            },
            "LOG_FILE": "python_docs_spider.log"
        }
    )
    process.crawl(PythonDocsSpider)
    process.start()
    with open(data_file, 'r') as f:
        data = json.load(f)
    data = sorted(data, key=lambda d : d['score'], reverse=True)
    ctr = 0
    print("URLS:")
    for d in data:
        if ctr > 5:
            break
        print(d['link'])
        ctr += 1

