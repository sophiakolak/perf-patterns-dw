from leet import HTMLParser
import mysql.connector
import requests
import ast
import os
import time

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)
mycursor = mydb.cursor(buffered=True)

def load_urls():
    f = open("urls.txt", "r+")
    contents = f.read()
    dic = ast.literal_eval(contents)
    return dic

def get_runtime_percentile(url):
    headers = HTMLParser.define_headers()
    time.sleep(0.01)
    r1 = requests.get(url, headers=headers)
    parser = HTMLParser()
    parser.feed(r1.text)
    return parser.data

def get_prob_number(prob_id):
    query = 'SELECT prob_number FROM array_problems WHERE id="'+prob_id+'"'
    mycursor.execute(query)
    result = mycursor.fetchone()
    return result[0]

def get_sample(prob_number, runtime):
    url = "https://leetcode.com/submissions/api/detail/"+prob_number+"/python3/"+runtime+"/"
    parser = HTMLParser()
    headers = HTMLParser.define_headers()
    time.sleep(0.01)
    r1 = requests.get(url, headers=headers)
    try:
        dic = ast.literal_eval(r1.text)
        return dic["code"]
    except:
        return None

def add_to_db(array_key, code, runtime, percentile):
    command = ("INSERT INTO samples "
            "(array_key, code, runtime, percentile) "
            "VALUES (%s, %s, %s, %s)")
    data = (array_key, code, runtime, percentile)
    mycursor.execute(command, data)
    print(command, data)
    mydb.commit()

url_dic = load_urls()
for prob_id,url in url_dic.items():
    arrays = get_runtime_percentile(url)
    print(arrays)
    prob_number = get_prob_number(str(prob_id))
    for val in arrays:
        runtime = val[0]
        percentile = val[1]
        code = get_sample(str(prob_number), str(runtime))
        if code is None:
            continue
        add_to_db(prob_id, code, runtime, percentile)
    time.sleep(5)