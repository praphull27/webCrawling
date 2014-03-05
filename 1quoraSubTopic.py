#PRAPHULL KUMAR (204271732)
#LAKSHMAN KRISHNAMOORTHY (604354810)
#ATHARAV (504271368)
#File to read about pages of the topics and crawl the child topics

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import os
import sys
import glob

url_stack = []
topic_stack = []
url_hash = {}
url_stack.append('/Biomedical-Engineering')
topic_stack.append('Biomedical Engineering')
file_names = open("topic_names.txt", mode='w')
file_urls = open("topic_urls.txt", mode='w')
file_url_list = open("list_topic_url.txt", mode='w')
child_parent={}
child_parent_url={}
child_parent['Biomedical Engineering'] = 0
child_parent_url['/Biomedical-Engineering'] = 0
name_str = ''
url_str = ''
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

def url_grabber(url):
	new_url=url
	
	browser.get(new_url)
	try:
		el = browser.find_element_by_xpath("//div[@class='row p0_5 light']/a")
		webdriver.ActionChains(browser).move_to_element(el).click(el).perform()
		time.sleep(2)
	except NoSuchElementException:
		pass
	
	html_source = browser.page_source
	soup = BeautifulSoup(html_source)
	all_spans = soup.find_all("div", class_="e_col side_col w2_5")
	try:
		all_childs = (all_spans[0]).find_all("div", class_="row related_topics_list p1")
		child_links = (all_childs[1]).find_all('a' , href=True)
		topics = (all_childs[1]).get_text("|", strip=True)
		sub_topics=topics.split("|")
		url_array_new = []
		topics_array_new = []
		for link in child_links:
			url_array_new.append(link['href'])
		for topic in sub_topics:
			topics_array_new.append(topic)
		return url_array_new, topics_array_new
	except:
		return 0, 0


while len(url_stack) != 0 :
	url = url_stack.pop()
	name = topic_stack.pop()
	url_hash[url] = 1
	link_url = "http://www.quora.com" + url + "/about?share=1"
	name_str = name
	name1 = name
	url_str = "http://www.quora.com" + url + "?share=1"
	url1 = url
	while child_parent[name1]!=0:
		name_str = child_parent[name1] + "\t" + name_str
		url_str = "http://www.quora.com" + child_parent_url[url1] + "?share=1" + "\t" + url_str
		url1 = child_parent_url[url1]
		name1 = child_parent[name1]
	file_names.write((name_str + "\n").encode('utf-8'))
	file_urls.write((url_str + "\n").encode('utf-8'))
	url_array, topics_array = url_grabber(link_url)
	if url_array != 0:
		for url_1 in url_array:
			url_stack.append(url_1)
			child_parent_url[url_1] = url
		for topic_1 in topics_array:
			topic_stack.append(topic_1)
			child_parent[topic_1] = name

for url in url_hash.keys():
	file_url_list.write((url + "\n").encode('utf-8'))

file_names.close()
file_urls.close()
file_url_list.close()
browser.quit()

