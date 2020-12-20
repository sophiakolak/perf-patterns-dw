import mysql.connector
import os
import numpy as np

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)
mycursor = mydb.cursor(buffered=True)

f = open('outlier_stats.txt', 'r')

ids = []
for line in f:
    if ':' in line:
        id = line.split(":")[0]
        ids.append(id)
    else:
        print(line)

unique_ids = set(ids)
ones, zeros = [],[]
for id in unique_ids:
    query = 'SELECT is_high_perf FROM samples WHERE id="'+str(id)+'"'
    mycursor.execute(query)
    result = mycursor.fetchone()[0]
    if result == 0:
        zeros.append(result)
    if result == 1:
        ones.append(result)
print("low", len(zeros))
print("high", len(ones))