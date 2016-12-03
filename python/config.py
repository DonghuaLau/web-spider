#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

g_config = None

class Config:

	filename = "conf/config.json"
	config_object = []
	conf_data = ""

	def __init__(self, filename = "conf/config.json"):
		self.filename = filename 

	def load(self):

		cf = open(self.filename, "rb")
		self.conf_data = cf.read()
		cf.close()
		self.config_object = json.loads(self.conf_data)

	def get(self, main, name = None):
		ret = any(main in key for key in self.config_object)
		if(ret == True):
			if(name == None):
				return self.config_object[main]

			ret = any(name in key for key in self.config_object[main])
			if(ret == True):
				return self.config_object[main][name]
			else:
				return None
		else:
			return None

	def print_config(self):
		print "Load configuration complete, config file: %s" % (self.filename)
		for key, value in self.config_object.iteritems():
			print "%s=%s" % (key, value)

def unit_test_1():

	conf = "path"
	value = g_config.get(conf)
	print "get g_config [%s]: %s" % (conf, value)

	conf = "timeout"
	value = g_config.get(conf)
	print "get g_config [%s]: %s" % (conf, value)

	conf = "hell"
	value = g_config.get(conf)
	print "get g_config [%s]: %s" % (conf, value)

def unit_test_2():

	__init__()

	conf = "timeout"
	value = g_config.get(conf)
	print "get g_config [%s]: %s" % (conf, value)

	conf = "hell"
	value = g_config.get(conf)
	print "get g_config [%s]: %s" % (conf, value)

	main = "amazon"
	name = "search_url_prefix"
	value = g_config.get(main, name)
	print "get g_config [%s/%s]: %s" % (main, name, value)

	main = "amazon"
	name = "price"
	value = g_config.get(main, name)
	print "get g_config [%s/%s]: %s" % (main, name, value)

def __init__():
	global g_config 
	if(g_config == None):
		g_config = Config()
		g_config.load()
		g_config.print_config()


__init__()

#print "--- unit_test_1 ---"
#unit_test_1()
#print "--- unit_test_2 ---"
#unit_test_2()

