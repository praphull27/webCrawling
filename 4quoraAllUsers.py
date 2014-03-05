#PRAPHULL KUMAR (204271732)
#LAKSHMAN KRISHNAMOORTHY (604354810)
#ATHARAV (504271368)
#This script will Get the details of all the users with list of followers and following people.

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import os
import sys
import glob
import csv

file_users_list = open("list_users.txt", mode='r')
users_list_whole = file_users_list.read()
users_list = users_list_whole.split("\n")

file_users_csv = open("users.csv", mode='wb')
csvwriter = csv.writer(file_users_csv, delimiter = ',')
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
count = 0

for user in users_list[:-1]:
	user_url = 'https://www.quora.com' + user + '?share=1'
	browser.get(user_url)
	html_source = browser.page_source
	soup = BeautifulSoup(html_source)

	topic_soup = soup.find_all(attrs={"href":user + "/topics"})
	topic_num = ''
	if(topic_soup != []):
		topic_soup_num = (topic_soup[0]).find_all("span")
		topic_num = (topic_soup_num[0]).get_text()

	blog_soup = soup.find_all(attrs={"href":user + "/blogs"})
	blog_num = ''
	if(blog_soup != []):
		blog_soup_num = (blog_soup[0]).find_all("span")
		blog_num = (blog_soup_num[0]).get_text()

	question_soup = soup.find_all(attrs={"href":user + "/questions"})
	question_num = ''
	if(question_soup != []):
		question_soup_num = (question_soup[0]).find_all("span")
		question_num = (question_soup_num[0]).get_text()

	answer_soup = soup.find_all(attrs={"href":user + "/answers"})
	answer_num = ''
	if(answer_soup != []):
		answer_soup_num = (answer_soup[0]).find_all("span")
		answer_num = (answer_soup_num[0]).get_text()

	log_soup = soup.find_all(attrs={"href":user + "/log"})
	log_num = ''
	if(log_soup != []):
		log_soup_num = (log_soup[0]).find_all("span")
		log_num = (log_soup_num[0]).get_text()

	follower_url = 'https://www.quora.com' + user + '/followers?share=1'
	browser.get(follower_url)
	src_updated = browser.page_source
	src = ""
	while src != src_updated:
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(0.25)
		src_updated = browser.page_source
	html_source = browser.page_source
	soup = BeautifulSoup(html_source)

	followers_soup = soup.find_all("div", class_="pagedlist_item")
	follower=''
	for f in followers_soup[:-1]:
		f_soup = f.find_all("a", class_="user", href=True)
		if(len(f_soup) != 0):
			fol_soup = f_soup[0]
			follower = 'https://www.quora.com' + fol_soup['href'] + '?share=1,' + follower
	follower = (follower[:-1]).encode("utf-8")

	following_url = 'https://www.quora.com' + user + '/following?share=1'
	browser.get(following_url)
	src_updated = browser.page_source
	src = ""
	while src != src_updated:
		src = src_updated
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(0.25)
		src_updated = browser.page_source
	html_source = browser.page_source
	soup = BeautifulSoup(html_source)

	following_soup = soup.find_all("div", class_="pagedlist_item")
	following=''
	for f in following_soup[:-1]:
		f_soup = f.find_all("a", class_="user", href=True)
		if(len(f_soup) != 0):
			fol_soup = f_soup[0]
			following = 'https://www.quora.com' + fol_soup['href'] + '?share=1,' + following
	following = (following[:-1]).encode("utf-8")

	data = [user_url, topic_num, blog_num, question_num, answer_num, log_num, follower, following]
	csvwriter.writerow(data)
	count += 1
	if count%100 == 0:
		print count
	elif count%10 == 0:
		print "."

file_users_csv.close()
file_users_list.close()
browser.quit()
