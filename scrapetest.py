import scrapy
import json
import re
import scrapy_splash

#Use request and callback method for each website
#ScrapySplash settings
SPLASH_URL = 'http://192.168.59.103:8050'
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

sino1 = 'https://www.sinobiological.com/searc h/by-category?keywords='
sino2 = '&categoryCode=1'
data = ' '


#Write code for search here using re 
#data needs to look at string and replace spaces between words with %20 as that's what sino uses for searches
#Then look at results and pick first result that's desc doesn't have ligand in the name, likely by looping through all entries 
#and ignoring those entries. Then picking the first one


class SinoCrawler(scrapy.Spider): 
    data = input('What are you looking for?  ')
    final_url = str(sino1 + data + sino2)
    
    name = 'Sino'
    #Final webs
    start_urls = [
        #sino2 + filler ,
        final_url 

    ]

#Request data from server
#goto url, needs data, go to server grab info sent to client
   
        
            

    def parse(self, response):
        for quote in response.xpath('//*[@id="commdity_main"]'):
            catalog = quote.css('span.catalog::text').get()
            yield {
                'Title' : quote.css('h1::text').get(),
                'Catalog' : quote.css('span.catalog::text').get(),
                #this is super jank but it works so nice
                'Expression System' : quote.xpath('//*[@id="generalInformationBody"]/div/div/div/div[2]/text()').re('HEK'),
                'Expression System1' : quote.xpath('//*[@id="generalInformationBody"]/div/div/div/div[2]/text()').re('Mouse'),
                'Expression System2' : quote.xpath('//*[@id="generalInformationBody"]/div/div/div/div[2]/text()').re('Bacul'),
                'Expression System3' : quote.xpath('//*[@id="generalInformationBody"]/div/div/div/div[2]/text()').re('Coli'),
                'Expression System3' : quote.xpath('//*[@id="generalInformationBody"]/div/div/div/div[2]/text()').re('Insect'),
             }
        
        url = 'https://www.sinobiological.com/Product/GetProductPrice'
        headers = {
        'Host':' www.sinobiological.com',
        'Connection':' keep-alive',
        
        'Pragma':' no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With':' XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin':' https://www.sinobiological.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        }
        yield scrapy_splash.SplashFormRequest(url, callback=self.splashparse, formdata={'Catalog': catalog.strip() }, headers=headers)
    #Catalog must be dependant on catalog found 
    
    def splashparse(self, response):
        
        raw_data = response.body
        data = json.loads(raw_data)

        yield {

        "OfferPrice" : re.findall('\'OfferPrice\': (.*?),',str(data)),
        "SizeNum" : re.findall('\'SizeNum\': (.*?),', str(data)),

        #Needs to search for list price and size num without returning key errors 
        #"SizeNum" : data["SKU"]['10774-H27H-B-20']['SizeNum']
        }

        
    
   
        #next_page = response.css('li.next a::attr("href")').get()
        #if next_page is not None:
            #yield response.follow(next_page, self.parse)
        
    