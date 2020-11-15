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

percentile_dic = {}
cut_off_dic = {}

def get_samples(prob_key):
    query = 'SELECT id, percentile, runtime FROM samples WHERE array_key="'+prob_key+'"'
    mycursor.execute(query)
    return mycursor.fetchall()

def get_samples_and_prob():
    query = 'SELECT id, runtime, array_key FROM samples'
    mycursor.execute(query)
    return mycursor.fetchall()

def get_problems():
    query = 'SELECT DISTINCT array_key FROM samples'
    mycursor.execute(query)
    return mycursor.fetchall()

def update_db(id, data):
    command = "UPDATE samples SET is_high_perf=%s WHERE id=%s "
    values = (data, id)
    try:
        mycursor.execute(command, values)
        mydb.commit()
    except:
        print(id)

def find_cut_off(a):
    sum = 0
    sortedA = a[a[:, 0].argsort()]
    index = 0
    for x in sortedA.T[1]:
        sum += float(x)
        if sum >= 50:
            return sortedA[index][0]
        index += 1

probs = get_problems()
for prob in get_problems():
    prob_key = str(prob[0])
    percentiles = get_samples(prob_key)
    sum = 0
    for r in percentiles:
        id = r[0]
        percentile = r[1]
        sum += percentile
    percentile_dic[prob_key] = sum

print(percentile_dic)

probs = get_problems()
for prob in get_problems():
    prob_key = str(prob[0])
    percentiles = get_samples(prob_key)
    speed, rank = [],[]
    for r in percentiles:
        id = r[0]
        percentile = r[1]
        runtime = r[2]
        total = float(percentile_dic[prob_key])
        curr = (percentile*100)/total
        speed.append(runtime)
        rank.append(curr)
    rt_percentile = np.column_stack((speed,rank))
    cut_off = find_cut_off(rt_percentile)
    cut_off_dic[prob_key] = cut_off


result = get_samples_and_prob()
for x in result:
    id = str(x[0])
    runtime = int(x[1])
    prob_key = str(x[2])
    cut_off = cut_off_dic[prob_key]
    high_perf = "0"
    if runtime < int(cut_off):
        high_perf = "1"
    update_db(id, high_perf)


