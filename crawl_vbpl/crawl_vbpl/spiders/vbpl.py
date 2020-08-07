import scrapy
from crawl_vbpl.items import CrawlVbplItem
from scrapy_splash import SplashRequest

cookie = {
        "Culture":"vi",
        "G_ENABLED_IDPS":"google",
        "__zlcmid":"zYjL3SrShSvU6C",
        "thuvienphapluatnew":"E5357374601F2272ABF5168549C05F4E25CF95EE68208D614D12BFD5B7ECF837814DB70CD5922E71C131E7675C0998BD211767ADA0F223725FF2FC0DDC9F34018FC7DE826C6BD09B60B3C9B3A64871B7576ED14625F3B81429EFC0B1128F109A133BE124A7809D5A57594CC38FF16866D03725AD7E90D8CB3F5BD3DBA76E78190631C1CAEE38271A6E8D5CA791B83D52ECD2F8C9776F9162A87D370D340FE985E7D3273257A32D3749326506AA8D9589DC9F9701",
        "dl_user":"U91GdVpHRjFkSFWW",
        "ASP.NET_SessionId":"kbp4vwd3powhquuhxmdpvfdt",
        "Cookie_VB":"close",
        "__utma":"173276988.268027361.1596798415.1596798415.1596798415.1",
        "__utmc":"173276988",
        "__utmz":"173276988.1596798415.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        "__utmt":"1",
        "__utmb":"173276988.4.9.1596798427561"
    }


script2 = """
function main(splash)
    assert(splash:go(args.url))
      assert(splash:wait(6))
      username = splash:select('input#Content_ThongTinVB_Support_usernameTextBox')
      password = splash:select('input#Content_ThongTinVB_Support_passwordTextBox')
      username:send_text("bandautu")
      password:send_text("bandautu")
      login_button = splash:select('input#Content_ThongTinVB_Support_loginButton')
      assert(splash:wait(3))
      login_button:click()
      assert(splash:wait(4))
      tai_ve_button = splash:select('span#Content_ThongTinVB_SpDoanload')
  	  tai_ve_button:click()
      assert(splash:wait(3))
      return {
        html = splash:html(),
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
        urls = []
        for item in x:
            if(item.find('?tab=7')!=-1):
                urls.append(item)
        for item in urls:
            yield SplashRequest(url=item, cookies=cookie,callback=self.parse_file, args={'lua_source': script2})

    def parse_file(self, response):

        file_name = response.css('div#tab8 span::text').get().strip()
        file_url = response.xpath('//*[@id="Content_ThongTinVB_vietnameseHyperLink"]/@href').get()
        print(file_url)
        print(file_name)
        # item = CrawlVbplItem()
        # item['file_urls'] = file_url
        # item['file_name'] = file_name
        # yield item


