from scrapy.spiders import Spider
import json
import scrapy
from scrapy.crawler import CrawlerProcess

HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) \
    Chrome/80.0.3987.116 Safari/537.36'}
Api_Key = '7f59af901d2d86f78a1fd60c1bf9426a' # '2827ed44c4e21ec313f7b086ae412420'

class ScienceDirect(Spider):
    name = 'ScienceDirect'

    def __init__(self):
        self.word_list = ["Transformer", "Bert", "LSTM", "attention"]
        self.word_list_tmp = ["Transformer", "Bert", "LSTM", "attention"]
        self.new_key_words = []

    def start_requests(self):

        keyword = self.word_list_tmp[0]
        # 构造 url
        # url = 'https://dblp.org/search?q='
        # url += keyword
        # url += '&h=1&format=json'
        self.word_list_tmp.pop(0)
        print("=== Key words to be crawl: ", self.word_list_tmp)
        #get 方法
        url = f'https://api.elsevier.com/content/search/sciencedirect?query={keyword}&apiKey={Api_Key}&httpAccept=application%2Fjson'

        # 创建 scrapy.Request 实例
        req = scrapy.Request(url=url, headers=HEADERS, callback=self.parse)
        yield req

    def parse(self, response):
        print('--------------------------')
        result = json.loads(response.text)
        print(result)
        print('--------------------------')


if __name__ == '__main__':
    process = CrawlerProcess()

    process.crawl(ScienceDirect)
    process.start()  # the script will block here until the crawling is finished
