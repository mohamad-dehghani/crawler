import scrapy
from tak3da.items import Tak3DaItem
import re


class SongSpider(scrapy.Spider):
    name = 'song'
    start_urls = ['http://tak3da.com/']

    def parse(self, response):
        print('-' * 100)
        urls = response.css('div.mores > a.readon::attr(href)').getall()
        for i, url in enumerate(urls):
            yield scrapy.Request(url=url, callback=self.parse_detalis)

        next_page = response.css('ul.pagination > li.active > a::text').get()
        if next_page is not None:
            next_page = int(next_page) + 1
            next_page = 'https://www.tak3da.com/page/' + str(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detalis(self, response):

        try:
            temp = response.css('div.main_middle_moldule_boxes > article> h1> a ::text ').get().strip()
            if (temp.startswith('دانلود آهنگ')):
                items = Tak3DaItem()
                items['singer'] = temp.split('به نام')[0][12:]
                items['title'] = temp.split('به نام')[1]

                txt = response.xpath('//div[@class="text-center"]//p[position() > 2][text()] ').get().strip()
                x = txt.replace('<br>', '').replace('<p style="text-align:center;">', '').replace('</p>', '')
                items['text'] = re.sub(r"<a.*</a>", "", x)

                yield items

        except Exception as e:
            print(e)


