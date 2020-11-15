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

query = 'SELECT id,array_key,runtime FROM samples'
mycursor.execute(query)
result = mycursor.fetchall()

id_dic = {}
ids = []
for x in result:
    id = x[0]
    ak = str(x[1])
    rt = x[2]
    if ak+rt in id_dic:
        #query = 'DELETE FROM samples WHERE id="'+str(id)+'"'
        #mycursor.execute(query)
        #mydb.commit()er
        ids.append(id)
    else:
        id_dic[ak+rt] = 1

print(ids)
print(len(ids))