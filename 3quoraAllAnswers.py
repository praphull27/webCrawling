#PRAPHULL KUMAR (204271732)
#LAKSHMAN KRISHNAMOORTHY (604354810)
#ATHARAV (504271368)
#This script will read all answer details from each question url

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import WebDriverException
import time
import os
import sys
import glob
import csv

file_topic_question = open("list_topic_question.txt", mode='r')
topic_question_whole_list = file_topic_question.read()
topic_question_array = topic_question_whole_list.split("\n")

file_answers_csv = open("answers.csv", mode='wb')
csvwriter = csv.writer(file_answers_csv, delimiter = ',')

users={}

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
count = 0

for topic_question in topic_question_array[:-1]:
	topic_question_list = topic_question.split("\t")
	topic = topic_question_list[0]
	question = topic_question_list[1]

	browser.get(question)
	
	src_updated = browser.page_source
	src = ""
	while src != src_updated:
		src = src_updated
		try:
			el = browser.find_elements_by_xpath("//span[contains(@class, 'answer_voters')]//a[contains(@class, 'more_link')]")
			for elm in el:
				loc = elm.location_once_scrolled_into_view
				elm.click()
				time.sleep(1)
		except (ElementNotVisibleException, WebDriverException):
			pass
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(1)
		src_updated = browser.page_source
	html_source = browser.page_source
	
	soup = BeautifulSoup(html_source)
	topic_list = ''
	topic_list_soup=soup.find_all("a", class_="topic_name")
	for topic_soup in topic_list_soup:
		topic_list = 'https://www.quora.com' + topic_soup['href'] + '?share=1,' + topic_list
	topic_list = (topic_list[:-1]).encode("utf-8")

	question_soup = soup.find_all("div", class_="row w4_5 question_details")
	question_text=''
	if question_soup != []:
		question_text = (question_soup[0]).get_text()
		question_text = (question_text.strip()).encode("utf-8")

	all_answers_soup_list = soup.find_all("div", class_="pagedlist_item")
	for all_answers_soup in all_answers_soup_list[:-1]:
		try:
			upvote_number_soup = all_answers_soup.find_all("a", class_="lil_button rate_up")
			upvote_number = (upvote_number_soup[0]).get_text()
		
			answer_wraper_soup = all_answers_soup.find_all("div", class_="answer_wrapper")
				
			answer_text_soup = (answer_wraper_soup[0]).find_all("div", class_="answer_content")
			answer_text = (answer_text_soup[0]).get_text()
			answer_text = (answer_text.strip()).encode("utf-8")

			answer_user_wrapper_soup = (answer_wraper_soup[0]).find_all("span", class_="answer_user_wrapper")

			user_answer_url_soup1 = (answer_user_wrapper_soup[0]).find_all('a' , href=True)
			
			user_answer_url=''
			if user_answer_url_soup1 != []:
				user_answer_url_soup = user_answer_url_soup1[0]
				user_answer_url = 'https://www.quora.com' + user_answer_url_soup['href'] + '?share=1'
				user_url_ans = user_answer_url_soup['href']
				users[user_url_ans] = 1

			answer_voters_soup = (answer_wraper_soup[0]).find_all("span", class_="answer_voters")
			
			answer_voters_url=''
			if answer_voters_soup != []:
				answer_voters_url_soup1 = (answer_voters_soup[0]).find_all('a' , href=True)
				for answer_voters_url_soup in answer_voters_url_soup1:
					answer_voters_url = 'https://www.quora.com' + answer_voters_url_soup['href'] + '?share=1,' + answer_voters_url
					voter_user = answer_voters_url_soup['href']
					users[voter_user] = 1
				answer_voters_url = (answer_voters_url[:-1]).encode("utf-8")

			date_soup1 = (answer_wraper_soup[0]).find_all("div", class_="row item_action_bar")
			date_soup2 = (date_soup1[0]).find_all("span", class_="answer_permalink")
			date = (date_soup2[0]).get_text()

			answer_id = (question + '-' + user_answer_url).encode("utf-8")
			user_answer_url = (user_answer_url).encode("utf-8")
			data = [answer_id, question, user_answer_url, date, upvote_number, answer_voters_url, topic_list, topic, question_text, answer_text]
			csvwriter.writerow(data)
		except (UnicodeEncodeError, UnicodeDecodeError, IndexError, NameError):
			pass
	count += 1
	if count%100 == 0:
		print count
		file_users_list = open("list_users.tmp.txt", mode='w')
		user_urls = users.keys()
		for user_url in user_urls:
			try:
				file_users_list.write((user_url + "\n").encode("utf-8"))
			except (UnicodeEncodeError, UnicodeDecodeError):
				pass
		file_users_list.close()
	elif count%10 == 0:
		print "."

file_answers_csv.close()
file_topic_question.close()
file_users_list = open("list_users.txt", mode='w')
user_urls = users.keys()
for user_url in user_urls:
	try:
		file_users_list.write((user_url + "\n").encode("utf-8"))
	except (UnicodeEncodeError, UnicodeDecodeError):
		pass
file_users_list.close()
browser.quit()
