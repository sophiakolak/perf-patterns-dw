import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import re
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=os.environ['mysql_pass'],
    database="leetcode"
)

mycursor = mydb.cursor(buffered=True)


def add_to_db(title, acc, diff, link, prob_number):
    command = ("INSERT INTO problems "
               "(title, acceptance, difficulty, link, prob_number) "
               "VALUES (%s, %s, %s, %s, %s)")
    data = (title, acc, diff, link, prob_number)
    mycursor.execute(command, data)
    # print(command, data)
    mydb.commit()

with open("lc_table.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    for row in rows:
        first_td = row.find('td')
        as_string = str(first_td)
        # all passed challenges have "ac" for accepted
        if re.search("ac", as_string):
            # extract difficulty
            span = row.find_all('span')
            difficulty = span[1].getText()

            # extract acceptance
            labels = row.find_all('td')
            acceptance = labels[4].getText()[:-1]

            # extract url
            href = row.find('a')
            as_string = str(href)
            after = as_string.split('href="')[1]
            link = after.split("\"")[0]

            # extract title
            labels = row.find_all('td')
            as_string = str(labels[2])
            after = as_string.partition('Title" value="')[2]
            title = after.partition('"><div')[0]

            # extract problem number
            labels = row.find_all('td')
            prob_number = labels[1].getText()

            # add to db
            print(title, acceptance, difficulty, link, prob_number)
            add_to_db(str(title), str(acceptance), str(difficulty), str(link), str(prob_number))