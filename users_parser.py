import time
import os
import sys
import glob
import csv

file_users_csv = open('users.csv', 'rb')
whole_file = csv.reader(file_users_csv, delimiter = ',')
for row in whole_file:
    user_id = row[0]
    number_of_topics = row[1]
    number_of_blogs = row[2]
    number_of_questions = row[3]
    number_of_answers = row[4]
    number_of_edits = row[5]
    followers = row[6]
    following = row[7]
