#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
  
class TEDSpider(scrapy.spiders.Spider):

    name = "ted"

    allowed_domains = ["www.ted.com"]
    start_urls = [
        "https://www.ted.com/"
    ]

    #allowed_domains = ["blog.csdn.net"]
    #start_urls = [
    #    "http://blog.csdn.net/"
    #]

    #def __init__(self, *args, **kwargs):
    #    super(TEDSpider, self).__init__(*args, **kwargs)
    #    self.proxy_pool = ['10.14.36.102:8080']

    #def get_request(self, url):
    #    req = Requst(url=url)
    #    if self.proxy_pool:
    #        req.meta['proxy'] = self.proxy_pool[0]
    #    return req

    def parse(self, response):
        print("=============")
        print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        # print(response.body_as_unicode())
        
        current_url = response.url #爬取时请求的url
        body = response.body  #返回的html
        unicode_body = response.body_as_unicode()#返回的html unicode编码
