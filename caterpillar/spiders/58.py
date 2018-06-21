import scrapy


class QuotesSpider(scrapy.Spider):
    name = "58"

    def start_requests(self):
        urls = [
            'http://cd.58.com/zufang/0/?PGTID=0d300008-0006-6aed-5720-56c36a4bda9b&ClickID=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = '58.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
