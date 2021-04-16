# w3spider.py

import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

class W3S(scrapy.Spider):
    name = 'w3spider'
    custom_settings = {'FEEDS':{'w3s.csv':{'format':'csv'}},
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'    
    }

    start_urls = ['https://www.w3schools.com/html/html_iframe.asp']

    def parse(self,response):

        title = response.xpath('/html/head/title/text()').get()

        initial_data = {
            'title' : title
        }

        iframe_url = response.xpath('//iframe[@title="W3Schools HTML Tutorial"]/@src').get()
        iframe_url = "https://www.w3schools.com/html/" + iframe_url

        yield Request(
            iframe_url, callback=self.parse_iframe, meta=initial_data
        )


    def parse_iframe(self,response):

        iframe_title = response.xpath('//div[@id="main"]//h1/span/text()').get()

        item = {'title' : response.meta.get('title'),
            'iframe_title' : iframe_title,
            }

        yield item

# main driver

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(W3S)
    process.start()
