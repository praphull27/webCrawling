#PRAPHULL KUMAR (204271732)
#LAKSHMAN KRISHNAMOORTHY (604354810)
#ATHARAV (504271368)
#This script will open all topics page and extract the question url

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import os
import sys
import glob

file_url_list = open("list_topic_url.txt", mode='r')
topic_url_whole_list = file_url_list.read()
file_url_list.close()
topic_url_array=topic_url_whole_list.split("\n")
file_topic_question = open("list_topic_question.txt", mode='w')
topic_question = {}
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)

count=0
for topic_name in topic_url_array[:-1]:
	topic_url = "http://www.quora.com" + topic_name + "?share=1"
	topic_question[topic_url] = {}
	browser.get(topic_url)
	src_updated = browser.page_source
	src = ""
	while src != src_updated:
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(2)
		src_updated = browser.page_source

	html_source = browser.page_source
	split_html = html_source.split("<h3>")
	count_url = 0
	for i in range(1,len(split_html)):
		part = split_html[i].split('</h3>')[0]
		part_soup = BeautifulSoup(part)
		if ("<div") in part:
			for link in part_soup.find_all('a' , href=True):
				link_url = "http://www.quora.com" + link['href'] + "?share=1"
				topic_question[topic_url][link_url] = 1
			count_url += 1
	print "Links Read for " + topic_name + ": " + str(count_url)
	count += 1

for topic in topic_question.keys():
	for question in topic_question[topic].keys():
		try:
			file_topic_question.write((topic + "\t" + question + '\n').encode('utf-8'))
		except (UnicodeEncodeError, UnicodeDecodeError):
			pass

		

file_topic_question.close()
browser.quit()
