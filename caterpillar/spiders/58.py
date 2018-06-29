import scrapy

from bs4 import BeautifulSoup

from caterpillar.items import House


class QuotesSpider(scrapy.Spider):

    name = '58'

    custom_settings = {
        'ITEM_PIPELINES': {
            'caterpillar.pipelines.HousePipeline': 400
        }
    }

    def start_requests(self):
        urls = [
            'http://cd.58.com/zufang/0/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        # crawl house detail
        house_list = soup.select('div.des > h2 > a:nth-of-type(1)')
        for house in house_list[:5]:
            house_detail_url = house['href']
            yield scrapy.Request(url=house_detail_url, callback=self.parse_detail)

        # crawl house list page
        page_urls = [
            url.attrs.get('href') for url in soup.select('div.pager > a')
            if url.attrs.get('href')
        ]
        for url in page_urls[:2]:
            yield scrapy.Request(url=url, callback=self.parse_list)

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

        img_list = soup.select('ul.house-pic-list > li > img')
        img_urls = [img.attrs['lazy_src'] for img in img_list]
        house_dict['imgs'] = img_urls

        if not house_dict.get('title'):
            return False

        house = House(
            source_url=response.url,
            **house_dict
        )
        return house
