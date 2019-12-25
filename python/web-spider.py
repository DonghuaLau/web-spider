#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from config import g_config
from logger import g_logger

from amazon_keyword_rank import AmazonKeywordRank

def redirect_stdout_to_file(filename):
	fp = open(filename, 'a+')
	fp.write("stdout and stderr init")
	sys.stdout = fp
	sys.stderr = fp
	return fp

def close_redirect_file(fp):
	fp.close()
	fp.write("stdout and stderr closed")

def __main__():
	stdout_file = 'log/stdout.log'
	stdout_fp = redirect_stdout_to_file(stdout_file):
	akr = AmazonKeywordRank()
	g_logger.info("application started.")
	akr.run()
	close_redirect_file(stdout_fp):

