import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from seleniumwire import webdriver
import os
import time
import re
import mysql.connector
from login import lc_login

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)

mycursor = mydb.cursor(buffered=True)

def update_db(id, graph_link):
    command = 'UPDATE problems SET graph_link="'+graph_link+'" WHERE id="'+id+'"'
    mycursor.execute(command)
    mydb.commit()

def get_link():
    command = "SELECT link, ID FROM problems WHERE ID>107"
    mycursor.execute(command)
    return mycursor.fetchall()

first_headers = {
    "authority": "leetcode.com",
    "method": "GET",
    "path": "/problemset/all/",
    "scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "cookie":" _ga=GA1.2.1624094984.1584035258; __atuvc=3%7C45; __cfduid=d38be6f49ec43470844b8037f6a7288121609442277; _gid=GA1.2.2144990227.1609442279; c_a_u=\"cmtyc24=:1kv6Mz:X2CQ1_L2Gsw8cnzqe0rDL9Ptgag\"; __cf_bm=fa250938981211976f6dc75b4000fa72d620ce17-1609456549-1800-Af+QlzjqI3/QiEP8CcYyIio3X/PUTiKHGmFIJa0Gi94SwnSMMqgG6kzfoN9WMmYcQmWjKZrjg/mewQI9LNNDv50=; csrftoken=tQGsq375x9MXNiEP6SLPVde2Wt7iNRfRo89kigtFP0MSlHuUiBb5aHanZqiXNdSZ; messages=\"c28cc3b23aac3d32fe6a8efd581483749e03a5c0$[[\"__json_message\"\0540\05425\054\"Successfully signed in as rkrsn.\"]\054[\"__json_message\"\0540\05425\054\"Successfully signed in as rkrsn.\"]\054[\"__json_message\"\0540\05425\054\"Successfully signed in as rkrsn.\"]\054[\"__json_message\"\0540\05425\054\"Successfully signed in as rkrsn.\"]\054[\"__json_message\"\0540\05425\054\"You have signed out.\"]\054[\"__json_message\"\0540\05425\054\"Successfully signed in as rkrsn.\"]]\"; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTA1MDA2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImZhZjMxYzM2NzcxZGUxOGU5NDg3MTMxM2U3ODYwYTljZTRiYzZmNmIiLCJpZCI6MTA1MDA2NiwiZW1haWwiOiJpLm0ucmFsa0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6InJrcnNuIiwidXNlcl9zbHVnIjoicmtyc24iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvaW1yYWxrL2F2YXRhcl8xNTIxNzQ2NjE1LnBuZyIsInJlZnJlc2hlZF9hdCI6MTYwOTQ1NjU1OSwiaXAiOiIxMDAuMzMuMTIxLjc4IiwiaWRlbnRpdHkiOiIxMDhhOWIzMTgzOGNmOWU1Zjg5ZTQ4OThkZTYzMjhmOSIsInNlc3Npb25faWQiOjUzMzcxODEsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.hyPCcmXwY4LrjT8jBd7bKE5l85uuy7fnBjCGmzIOJPo",
    "referer": "https://leetcode.com/",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36"
}

headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "cookie": "__cfduid=d54493c5a593789f464efa0e9f2329aa51604155525; __cf_bm=1735af4b07d7f392aa571f0d2a3b3db4d582258b-1604155525-1800-ARtu/7bW6bIY5SOiVgGYCllIderDVQFAI+GMeIJXnGqoCPr7i+yWuHob9mSXP0HSXY2opCt9Ie0ZYmZ6mKU5M6U=; csrftoken=D1kDxnggpG56mUgHtO9UX4wyXB5yvI9uu10FFuDQqEtcTnQ7fwnMRE8FJBMWODmQ; messages=\"653c35088e484ab69d9d7bdebb0635f59766dbf5$[[\\\"__json_message\\\"\\0540\\05425\\054\\\"Successfully signed in as rkrsn.\\\"]]\"; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTA1MDA2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImNmMDAzYzY2MjFiY2MyNjNmNjNmZDc1NWJjYjg5YzY1OTAyZjI1NzMiLCJpZCI6MTA1MDA2NiwiZW1haWwiOiJpLm0ucmFsa0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6InJrcnNuIiwidXNlcl9zbHVnIjoicmtyc24iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvaW1yYWxrL2F2YXRhcl8xNTIxNzQ2NjE1LnBuZyIsInJlZnJlc2hlZF9hdCI6MTYwNDE1NTY3NSwiaXAiOiI3My44OC4yMzUuMzEiLCJpZGVudGl0eSI6IjNhMzlhMWQ2NjEzNzgyM2YzNjdkMDQ4Mjk0MGJkN2I4Iiwic2Vzc2lvbl9pZCI6MzU5NjcxNiwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwfQ.vVpsgd7xM7wpcR8q3IKFdiU8rdqHzfMzCnyFInCXh0s",
        "referrer": "https://leetcode.com/accounts/login/?next=/submissions/detail/182745087/",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": None,
        "method": "GET",
        "mode": "cors"
}
cookie = "_ga=GA1.2.1624094984.1584035258; __atuvc=3%7C45; __cfduid=d38be6f49ec43470844b8037f6a7288121609442277; __cf_bm=73daa37e82b6634c5809001de9d40d4f472d96f8-1609442277-1800-Ad8GSCb+i889cIeBUjO2s7IMlMW7+Ly1oh5oSRGRUmDWaYazQLYZ3BUqG1MOdf17h6xhWaTnuf21D2pTDDB47Co=; _gid=GA1.2.2144990227.1609442279; _gat=1; csrftoken=KzB2MNGwm4Gt7xqFuqkXtMcxYrZbBg30B1cw9gT5oaAfyoPpCLuikCkzZz0P4oNp; messages=\"653c35088e484ab69d9d7bdebb0635f59766dbf5$[[\"__json_message\"\0540\05425\054\"Successfully signed in as rkrsn.\"]]\"; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiMTA1MDA2NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImZhZjMxYzM2NzcxZGUxOGU5NDg3MTMxM2U3ODYwYTljZTRiYzZmNmIiLCJpZCI6MTA1MDA2NiwiZW1haWwiOiJpLm0ucmFsa0BnbWFpbC5jb20iLCJ1c2VybmFtZSI6InJrcnNuIiwidXNlcl9zbHVnIjoicmtyc24iLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvaW1yYWxrL2F2YXRhcl8xNTIxNzQ2NjE1LnBuZyIsInJlZnJlc2hlZF9hdCI6MTYwOTQ0MjI4NiwiaXAiOiIxMDAuMzMuMTIxLjc4IiwiaWRlbnRpdHkiOiI1MzhmYjdlZmEwY2RlMTQ3YWRmMTBmZjBjYmY1NGRjZSIsInNlc3Npb25faWQiOjUzMzQ1NzIsIl9zZXNzaW9uX2V4cGlyeSI6MTIwOTYwMH0.8Y8L4iP0no9-Dda72A4Y5y_CGsHEkLrZiQgXVrg99eU"
headers["cookie"] = cookie


driver = webdriver.Firefox()
lc_login(driver)
base = "https://leetcode.com"
#driver.header_overrides = first_headers
driver.get(base+"/problemset/all/")
time.sleep(2)
result = get_link()
for prob_path in result:
    id = prob_path[1]
    full_path = base+prob_path[0]+"/submissions/"
    headers["referrer"] = base + prob_path[0]
    #driver.header_overrides = headers
    driver.get(full_path)
    #time for javascript to load
    time.sleep(15)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')[1:]
    for row in rows:
        print(row)
        vals = row.find_all('td')
        lang = vals[4].getText()
        status = vals[1].find('a').getText()
        if lang == 'python' or lang == 'python3' and status == 'Accepted':
            as_string = str(vals[1].find('a'))
            after = as_string.partition('href="')[2]
            graph_link = after.partition('" target')[0]
            update_db(str(id), graph_link)