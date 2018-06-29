import scrapy

from bs4 import BeautifulSoup

from ..items import House


class QuotesSpider(scrapy.Spider):
    name = '58'

    custom_settings = {
        'ITEM_PIPELINES': {
            'caterpillar.pipelines.HousePipeline': 400
        }
    }

    def start_requests(self):
        urls = [
            # 'http://cd.58.com/zufang/0/'
            'http://cd.58.com/zufang/34540463083843x.shtml?from=1-list-0&iuType=z_0&PGTID=0d300008-0006-63f5-4dbf-7dd529e9b1dd&ClickID=2&adtype=3'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_list(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        house_list = soup.select('div.des > h2 > a')

        for house in house_list:
            house_detail_url = house['href']
            yield scrapy.Request(url=house_detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        house_dict = dict(
            title=soup.select_one('div.house-title > h1'),
            price=soup.select_one('div.house-pay-way > span > b'),
            payment=soup.select_one('div.house-pay-way > span:nth-of-type(2)'),
            house_type=soup.select_one('div.house-desc-item > ul > li:nth-of-type(2) > span:nth-of-type(2)'),
            house_community=soup.select_one('div.house-desc-item > ul > li:nth-of-type(4) > span:nth-of-type(2)'),
            region=soup.select_one('div.house-desc-item > ul > li:nth-of-type(5) > span:nth-of-type(2)'),
            address=soup.select_one('div.house-desc-item > ul > li:nth-of-type(6) > span:nth-of-type(2)'),
            desc=soup.select_one('ul.introduce-item > li:nth-of-type(2) > span:nth-of-type(2)'),
        )
        house_dict = {
            key: value.text.replace('\n', '').replace('\xa0\xa0', '').replace(' ', '')
            for key, value in house_dict.items() if value
        }
        import ipdb; ipdb.set_trace()

        img_list = soup.select('ul.house-pic-list > li > img')
        img_urls = [img.attrs['lazy_src'] for img in img_list]
        house_dict['imgs'] = img_urls

        house = House(
            source_url=response.url,
            **house_dict
        )
        return house
