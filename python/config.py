import json

class Config:

	filename = "config.json"
	config_object = []
	conf_data = ""

	def __init__(self, filename = "config.json"):
		self.filename = filename 

	def load(self):

		cf = open(self.filename, "rb")
		self.conf_data = cf.read()
		cf.close()
		self.config_object = json.loads(self.conf_data)

	def get(self, name):
		ret = any(name in key for key in self.config_object)
		if( ret == True):
			return self.config_object[name]
		else:
			return ""

	def print_config(self):
		for key, value in self.config_object.iteritems():
			print "[%s=%s]" % (key, value)


def unit_test_1():
	config = Config()
	config.load()
	config.print_config()
	
	print "===================" 

	conf = "path"
	value = config.get(conf)
	print "get config [%s]: %s" % (conf, value)

	conf = "timeout"
	value = config.get(conf)
	print "get config [%s]: %s" % (conf, value)

	conf = "hell"
	value = config.get(conf)
	print "get config [%s]: %s" % (conf, value)

def unit_test_2():
	config = Config("conf.json")
	config.load()
	config.print_config()
	
	print "===================" 

	conf = "path"
	value = config.get(conf)
	print "get config [%s]: %s" % (conf, value)

	conf = "timeout"
	value = config.get(conf)
	print "get config [%s]: %s" % (conf, value)

	conf = "hell"
	value = config.get(conf)
	print "get config [%s]: %s" % (conf, value)


#print "--- unit_test_1 ---"
#unit_test_1()
#print "--- unit_test_2 ---"
#unit_test_2()

