from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
import sys
import json

def save_html_page(page_source, filename):
	f = open(filename, 'wb')
	f.write(page_source)
	f.close()

def amazon_product_search(url):
	try:
		browser = webdriver.PhantomJS('/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
		browser.get(url)
		print("[get] %s" % url)
		#print("[main] text: %s" % browser.text)
		browser.implicitly_wait(1)

		filename = "amazon_search_iphone.html"
		source = browser.page_source.encode('utf-8')
		print("[page] source filename: %s" % filename)
		save_html_page(source, filename)

		elem_id = "s-results-list-atf"
		results_list = browser.find_element_by_id(elem_id)
		print("[find element] id: %s" % elem_id)

		# screenshot
		filename = "amazon_search_iphone.png"
		results_list.screenshot(filename)
		#base64_png = results_list.screenshot_as_png()
		print("[screenshot] %s" % filename)


		#tag_name = "h2"
		#title = results_list.find_elements_by_tag_name(tag_name)
		#print("[find element] tag name: %s" % tag_name)

		#i = 0
		#for t in title:
		#	i += 1
		#	print("%d: %s" % (i, t.text))
		#	#print(i)
		#	#print(t.text)

		title_link_class = "s-access-detail-page"
		title_link_xpath = "./div/div/div/div/div/a"

		tag_name = "li"
		title_xpath = "./li/div/div/div/div/div/a"
		#results = results_list.find_elements_by_tag_name(tag_name)
		#results = results_list.find_elements_by_xpath(title_xpath)
		results = results_list.find_elements_by_class_name(title_link_class)
		print("[find element] tag name: %s" % tag_name)
		print("[find element] title xpath: %s" % title_xpath)
		#print(results)


		i = 0
		for res in results:
			i += 1

			print("[title] get title link")

			#print(json.dumps([ob.__dict__ for ob in res]))
			#title_elem = res.find_element_by_class_name(title_link_class)
			#title_elem = res.find_element_by_xpath(title_link_xpath)
			#print title_elem.page_source
			#title_name = title_elem.get_attribute("title")
			#title_link = title_elem.get_attribute("href")
			#print("[title] %d, title: %s, link: %s" % (i, title_name, title_link))

			title_name = res.get_attribute("title")
			title_link = res.get_attribute("href")
			print("[title] %d, title: %s, link: %s" % (i, title_name, title_link))


		print("[finished]")

	except NoSuchElementException as err: 
		print("unexpected error: %s" % sys.exc_info()[0])
		#print("unexpected error 0: %s" % err.exc_info()[0])
		#print("unexpected error 1: %s" % err.exc_info()[1])

	except AttributeError as err: 
		print("unexpected error: %s" % sys.exc_info()[0])

	except:
		print("unexpected error: %s" % sys.exc_info()[0])
	
	browser.quit()

url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=led+light'
url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=iphone'
url = 'https://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=C%2B%2B+primer&rh=i%3Aaps%2Ck%3AC%2B%2B+primer'
#url = 'https://www.amazon.cn/gp/search/ref=sr_pg_2?rh=i%3Aaps%2Ck%3AC%2B%2B+primer&page=2&keywords=C%2B%2B+primer&ie=UTF8&qid=1480492557'
#url = 'http://liudonghua.net/download/amazon/search_iphone.html'
amazon_product_search(url)
