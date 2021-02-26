import scrapy

from scrapy.loader import ItemLoader
from ..items import ResursbankItem
from itemloaders.processors import TakeFirst


class ResursbankSpider(scrapy.Spider):
	name = 'resursbank'
	start_urls = ['https://www.resursbank.no/om-oss/presse-media/pressemeldinger']

	def parse(self, response):
		post_links = response.xpath('//div[@class="cision-feed-item--content"]')
		for post in post_links:
			date = post.xpath('.//p[@class="cision-feed-item--content--date"]/text()').get()
			url = post.xpath('./a[@class="link--default  "]/@href').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//div[@class="single-cision-item"]/h3/text()').get()
		description = response.xpath('//div[@class="single-cision-item--intro" or @class="single-cision-item--body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=ResursbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
