from scrapy.spiders import Spider
import json
import scrapy
from scrapy.crawler import CrawlerProcess
from ScienceDirectSpider.items import SciencedirectspiderItem
import re
import time as T

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/80.0.3987.116 Safari/537.36'}
HEADERS_AUTH = {'Content-Type': 'application/json', 'Accept': 'application/json', 'x-els-apikey': '7f59af901d2d86f78a1fd60c1bf9426a',}
HEADER_POST ={}
HEADER_POST.update(HEADERS)
HEADER_POST.update(HEADERS_AUTH)
Api_Key = '7f59af901d2d86f78a1fd60c1bf9426a' # '2827ed44c4e21ec313f7b086ae412420'

class ScienceDirect(Spider):
    name = 'ScienceDirect'

    def __init__(self):
        self.word_list = ["Transformer", "Bert", "LSTM", "attention"]
        self.word_list_tmp = ["Transformer", "Bert", "LSTM", "attention"]
        self.new_key_words = []
        self.paper_list = []

    def start_requests(self):

        keyword = self.word_list_tmp[0]

        self.word_list_tmp.pop(0)
        # 构造url, get 方法
        url = f'https://api.elsevier.com/content/search/sciencedirect?query={keyword}&count=100&apiKey={Api_Key}&httpAccept=application%2Fjson'
        #url = 'https://api.elsevier.com/content/search/sciencedirect?start=5900&count=100&query=Transformer&apiKey=7f59af901d2d86f78a1fd60c1bf9426a&httpAccept=application%2Fjson'
        # 创建 scrapy.Request 实例
        req = scrapy.Request(url=url, headers=HEADERS, callback=self.parse)
        yield req

    def parse(self, response):
        paper_list_tmp = []

        item = SciencedirectspiderItem()
        result = json.loads(response.text)
        result = result["search-results"]
        links = result["link"]
        entry = result["entry"]
        print('--------------------------')
        now_link = links[0]['@href']
        next_link = [x for x in links if x['@ref'] == 'next']
        if len(next_link)>0:
            next_link = next_link[0]['@href']
        else:
            next_link = now_link
        page = re.findall(r"start=(.+?)&",string=now_link)
        word = re.findall(r"query=(.+?)&",string=now_link)
        print(f'now crawling word {word}, page {page} of 6000')


        for paper in entry:
            item['title'] = paper[r'dc:title']
            if paper[r'dc:title'] in self.paper_list:
                continue
            self.paper_list.append(item['title'])
            paper_list_tmp.append(item['title'])
            try:
                authors = paper['authors']['author']
                if type(authors) == type(str()):
                    item['authors'] = authors
                else:
                    item['authors'] = [x["$"] for x in authors]
            except:
                item['authors'] = ''

            item['doi'] = paper['prism:doi']
            item['url'] = paper['link'][0]['@href']
            time = paper['load-date'].split('-')
            item['year'] = time[0]
            item['month'] = time[1]
            item['venue'] = paper['prism:publicationName']
            item['source'] = 'ScienceDirect'
            yield item


        for title in paper_list_tmp:
            words = title.split(' ')
            for word in words:
                if (len(word)>5 or (word.isupper() and len(word)>2)) and len(self.word_list_tmp)<1000:
                    if word in self.word_list:
                        continue
                    self.word_list.append(word)
                    self.word_list_tmp.append(word)


        print('--------------------------')
        print(f'words to crawl = {len(self.word_list_tmp)}:')

        if not now_link == links[3]['@href']:
            # T.sleep(0.5)
            req = scrapy.Request(url=next_link, headers=HEADERS, callback=self.parse)
            yield req
        else:
            url = f'https://api.elsevier.com/content/search/sciencedirect?query={self.word_list_tmp.pop(0)}&count=100&apiKey={Api_Key}&httpAccept=application%2Fjson'
            req = scrapy.Request(url=url, headers=HEADERS, callback=self.parse)
            yield req



if __name__ == '__main__':
    # 便于调试，输出item到指定文件和指定打印日志等级
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
        "LOG_LEVEL" : "INFO"
    })

    process.crawl(ScienceDirect)
    process.start()  # the script will block here until the crawling is finished
