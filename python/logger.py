#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler
from config import g_config

g_logger = None

# 104857600 = 100MB
def logging_init(log_file, log_level, max_filesize = 104857600):
	global g_logger
	log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
	log_handler = RotatingFileHandler(log_file, mode='a', maxBytes=max_filesize, 
	                                 backupCount=5, encoding=None, delay=0)
	log_handler.setFormatter(log_formatter)
	log_handler.setLevel(log_level)
	g_logger = logging.getLogger('root')
	g_logger.setLevel(log_level)
	g_logger.addHandler(log_handler)
	g_logger.info("logging init")

def unit_test_1():
	
	for n in range(0, 10000):
		g_logger.info("info log: %d", n)
		g_logger.log(logging.DEBUG, "debug log: %d", n)
		g_logger.warning("warning log: %d", n)
		g_logger.error("error log: %d", n)

def __init__():

	if(g_logger == None):
		log_file = g_config.get("log", "path") + "/" + g_config.get("log", "filename")
		log_level = g_config.get("log", "level")
		max_filesize = g_config.get("log", "max_filesize")
		logging_init(log_file, log_level, max_filesize)

		# log level
		g_logger.DEBUG = logging.DEBUG

__init__()
#unit_test_1()


