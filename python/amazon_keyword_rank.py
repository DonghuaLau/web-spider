#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 

from config import g_config
from logger import g_logger
import utils

class AmazonKeywordRank:

	_phantomjs = 'phantomjs'	
	_temp_dir = 'temp/'

	_product_rank = 0
	_keywords = ''
	_search_url_prefix = ''
	_search_url = '' # _search_url_prefix + keyword

	def __init__(self):
		self._keywords = g_config.get('amazon', 'keywords')
		self._search_url_prefix = g_config.get('amazon', 'search_url_prefix')
		if(g_config.get('phantomjs') != None):
			self._phantomjs = g_config.get('phantomjs')	
		else:
			g_logger.warning("not config phantomjs path")

		if(g_config.get('temp_dir') != None):
			self._temp_dir = g_config.get('temp_dir')	

		# urlencode keywords
		length = len(self._keywords)
		for i in range(length):
			self._keywords[i] = urllib.quote(self._keywords[i])
			g_logger.log(g_logger.DEBUG, "keyword: %s" % self._keywords[i])
		g_logger.log(g_logger.DEBUG, "AmazonKeywordRank init, keywords: ")
		g_logger.log(g_logger.DEBUG, self._keywords)
		g_logger.log(g_logger.DEBUG, "AmazonKeywordRank init, search_url_prefix: %s" , self._search_url_prefix)
		g_logger.log(g_logger.DEBUG, "AmazonKeywordRank init, phantomjs: %s" , self._phantomjs)

	def run(self):
		url = ''
		for keyword in self._keywords:
			url = self._search_url_prefix + keyword
			self.amazon_keyword_search(keyword)

	def amazon_keyword_search(self, keyword):
		url = self._search_url_prefix + keyword
		g_logger.log(g_logger.DEBUG, "keyword search URL: %s" % url)
		try:
			browser = webdriver.PhantomJS(self._phantomjs)
			browser.get(url)
			g_logger.log(g_logger.DEBUG, "[get] %s" % url)
			#g_logger.log(g_logger.DEBUG, "[main] text: %s" % browser.text)
			browser.implicitly_wait(1)
	
			# save source page
			filename = self._temp_dir + "/" + keyword + ".html"
			source = browser.page_source.encode('utf-8')
			g_logger.log(g_logger.DEBUG, "[page] source filename: %s" % filename)
			utils.save_html_page(source, filename)
	
			elem_id = "s-results-list-atf"
			results_list = browser.find_element_by_id(elem_id)
			g_logger.log(g_logger.DEBUG, "[find element] id: %s" % elem_id)
	
			# screenshot
			filename = self._temp_dir + "/" + keyword + ".png"
			results_list.screenshot(filename)
			g_logger.log(g_logger.DEBUG, "[screenshot] %s" % filename)
	
			title_link_class = "s-access-detail-page"
			title_link_xpath = "./div/div/div/div/div/a"
	
			tag_name = "li"
			title_xpath = "./li/div/div/div/div/div/a"
			results = results_list.find_elements_by_class_name(title_link_class)
			g_logger.log(g_logger.DEBUG, "[find element] tag name: %s" % tag_name)
			g_logger.log(g_logger.DEBUG, "[find element] title xpath: %s" % title_xpath)
	
			i = 0
			for res in results:
				i += 1
	
				g_logger.log(g_logger.DEBUG, "[title] get title link")
	
				title_name = res.get_attribute("title")
				title_link = res.get_attribute("href")
				g_logger.log(g_logger.DEBUG, "[title] %d, title: %s, link: %s" % (i, title_name, title_link))
	
	
			g_logger.log(g_logger.DEBUG, "[finished]")
	
		except NoSuchElementException as err: 
			g_logger.log(g_logger.DEBUG, "unexpected error: %s" % sys.exc_info()[0])
	
		except AttributeError as err: 
			g_logger.log(g_logger.DEBUG, "unexpected error: %s" % sys.exc_info()[0])
	
		except:
			g_logger.log(g_logger.DEBUG, "unexpected error: %s" % sys.exc_info()[0])
		
		browser.quit()

	
