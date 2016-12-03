#!/usr/bin/python
# -*- coding: utf-8 -*-

def save_to_file(content, filename):
	f = open(filename, 'wb')
	f.write(content)
	f.close()

def save_html_source(browser, filename):
	source = browser.page_source.encode('utf-8')
	save_to_file(source, filename)

def save_page_screenshot(browser, filename):
	browser.screenshot(filename)

