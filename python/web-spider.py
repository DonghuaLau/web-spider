#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import g_config
from logger import g_logger

from amazon_keyword_rank import AmazonKeywordRank

def run():
	# do something
	akr = AmazonKeywordRank()
	g_logger.info("application started.")
	akr.run()

run()

