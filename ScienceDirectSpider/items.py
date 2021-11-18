# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SciencedirectspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    abstract = scrapy.Field()
    authors = scrapy.Field()
    doi = scrapy.Field()
    url = scrapy.Field()
    year = scrapy.Field()
    month = scrapy.Field()
    type = scrapy.Field()
    venue = scrapy.Field()
    source = scrapy.Field()
    video_url = scrapy.Field()
    video_path = scrapy.Field()
    thumbnail_url = scrapy.Field() # 视频略缩图
    pdf_url = scrapy.Field()
    pdf_path = scrapy.Field()
    inCitations = scrapy.Field()
    outCitations = scrapy.Field()

    pass
