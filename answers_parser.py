import time
import os
import sys
import glob
import csv

file_answers_csv = open('answers.csv', 'rb')
whole_file = csv.reader(file_answers_csv, delimiter = ',')
for row in whole_file:
    answer_id = row[0]
    question_id = row[1]
    user_id = row[2]
    date = row[3]
    number_of_upvotes = row[4]
    users_who_upvoted = row[5]
    topics = row[6]
    current_topics = row[7]
    question_text = row[8]
    answer_text = row[9]
