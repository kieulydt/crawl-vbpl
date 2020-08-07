import scrapy
from crawl_vbpl.items import CrawlVbplItem
from scrapy_splash import SplashRequest

cookie = {
        "Culture":"vi",
        "G_ENABLED_IDPS":"google",
        "__zlcmid":"zYjL3SrShSvU6C",
        "thuvienphapluatnew":"E90C322C9F718303F23B0BC2198073735BF338B7E3BBC1E78D16CB4DD4EA29BA4E8650EAFBBFF5A28126B73AF03D559B78D855DA8C87DE184B786E2EE09A0B43CD6D768F6863D3D9490E2CD831B4AD92C037BBF3ACF9C8611D6DCC7964D767F6696F8378C7ECB2BC4ACD12EBEEA1E091D81432710973B6049790DF10555CB37853763B4C3E44F638C1D2377B66906727C39EB3EF197D967E7B7C326517F5F3DBE4AC36F137FD630CFDFFFB1DC5B3B495E71085B4",
        "dl_user":"U91GdVpHRjFkSFWW",
        "ASP.NET_SessionId":"kbp4vwd3powhquuhxmdpvfdt",
        "Cookie_VB":"close",
        "__utma":"19472893.943406357.1596771235.1596771235.1596771235.1",
        "__utmc":"19472893",
        "__utmz":"19472893.1596771235.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        "__utmt":"1",
        "__utmb":"19472893.3.8.1596771235"
    }


script2 = """
function main(splash)
    assert(splash:go(url))
    assert(splash:wait(0.5))
    urls = splash:select('a#Content_ThongTinVB_vietnameseHyperLink')
        urls:click()
    assert(splash:wait(3))
    return {
        
        html = splash:html()
    }
end
"""

class VbplSpider(scrapy.Spider):
    name = 'vbpl'
    allowed_domains = ['thuvienphapluat.vn']
    start_urls = ['https://thuvienphapluat.vn/phap-luat/tim-van-ban.aspx?keyword=&area=0&match=True&type=0&status=0&signer=0&sort=1&lan=1&scan=0&org=0&fields=0#']

    def start_request(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies= cookie, callback=self.parse)

    def parse(self, response):
        for i in range(11632):
            url = 'https://thuvienphapluat.vn/phap-luat/tim-van-ban.aspx?keyword=&area=0&match=True&type=0&status=0&signer=0&sort=1&lan=1&scan=0&org=0&fields=0&page=' + str(i)
            yield scrapy.Request(url=url, cookies=cookie, callback=self.parse_item)

    def parse_item(self, response):
        # print(response.url)
        x = response.css('div.content-0 div.nq p.links-bot a::attr(href)').extract()
        # print(x)
        urls = []
        for item in x:
            if(item.find('?tab=7')!=-1):
                urls.append(item)
        for item in urls:
            # requests.meta['url'] = item
            yield SplashRequest(url=item, cookies=cookie, callback=self.parse_file, args={'lua_source':script2})

    def parse_file(self, response):

        file_name = response.css('div#tab8 span::text').get().strip()
        file_url = response.xpath('//*[@id="Content_ThongTinVB_vietnameseHyperLink"]/@href').get()
        print(file_url)
        print(file_name)
        # item = CrawlVbplItem()
        # item['file_urls'] = file_url
        # item['file_name'] = file_name
        # yield item


