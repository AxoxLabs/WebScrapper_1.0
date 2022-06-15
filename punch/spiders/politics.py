from unicodedata import category
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PoliticsSpider(CrawlSpider):
    name = 'politics'
    allowed_domains = ['punchng.com']
  

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://punchng.com/topics/politics', headers={
            'User-Agent': self.user_agent
        })

   
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h1[@class='post-title']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
         Rule(LinkExtractor(restrict_xpaths="//h3[@class='entry-title']/a"), callback='parse_item', follow=True, process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request


    def parse_item(self, response):
        newspaper = "Punch Newspaper"
        category = "Politics"
        yield {
            'headine': response.xpath("////h1[@class='post-title']/text()").get(),
            'image_url': response.xpath("//div[@class='post-image-wrapper']/figure/img/@src").get(),
            'authour': response.xpath("(//span[@class='post-author']/strong)[1]/text()").get(),
            'posted_date':response.xpath("//span[@class='post-date']/text()").get(),
            'description': response.xpath("(//div[@class='post-content']/p)[1]/text()").get(),
            'newspaper_name': newspaper,
            'category': category,
            'url': response.url
           
        }
        

