#!/usr/bin/python
# -*- coding: utf-8 -*-

def save_html_page(page_source, filename):
	f = open(filename, 'wb')
	f.write(page_source)
	f.close()
