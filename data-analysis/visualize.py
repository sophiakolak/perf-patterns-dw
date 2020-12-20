import mysql.connector
import os
# from staticfg import CFGBuilder
import tokenize
import ast
import json
from pprint import pprint
from collections import Counter
# from graphviz import Digraph
from networkx import nx
from matplotlib.pyplot import figure
from collections import Counter
import matplotlib
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cluster import DBSCAN
from sklearn import svm

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)
mycursor = mydb.cursor(buffered=True)
upper_lower_dic = {}
X = np.array([])
y = np.array([])

def get_samples(prob_key):
    query = 'SELECT id, deepwalk, is_high_perf FROM samples WHERE array_key="'+prob_key+'"'
    mycursor.execute(query)
    return mycursor.fetchall()

def parse_data(vecs):
    sep = vecs.split(" ")
    num_nodes = int(sep[0])
    dim = int(sep[1].split("\n")[0])
    n1 = sep[1].split("\n")[1]
    node = vecs.split('\n')
    node.pop(0)
    X = []
    for embed in node:
        nums = embed.split(" ")
        if len(nums) > 1:
            [float(i) if '.' in i else int(i) for i in nums]
            X.append(nums[1:len(nums)-1])
    return X[1:]

def select_problems():
    query = 'SELECT DISTINCT array_key FROM samples'
    mycursor.execute(query)
    result = mycursor.fetchall()
    #for x in result:
    #    prob_key = str(x[0])
    #    upper_lower_dic[prob_key] = get_upper_lower(prob_key)
    for x in result:
        prob_key = str(x[0])
        #visualize_samples(prob_key)
        predict_samples(prob_key)

def calc_upper_lower(list):
    sorted(list)
    q1, q3 = np.percentile(list, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)
    return upper_bound, lower_bound

def quantiles(all_points):
    x_vals, y_vals = [],[]
    for point in all_points:
        x_vals.append(point[0])
        y_vals.append(point[1])
    x_u, x_l = calc_upper_lower(x_vals)
    y_u, y_l = calc_upper_lower(y_vals)
    return (x_u, x_l), (y_u, y_l)

def check_outlier_1D(prob_key, point):
    x_upper, x_lower = upper_lower_dic[prob_key][0]
    y_upper, y_lower = upper_lower_dic[prob_key][1]
    x, y = point
    if x < x_lower or x > x_upper:
        return True
    if y < y_lower or y > y_upper:
        return True
    return False

def check_outlier_2D(prob_key, point):
    x_upper, x_lower = upper_lower_dic[prob_key][0]
    y_upper, y_lower = upper_lower_dic[prob_key][1]
    x, y = point
    x_outlier, y_outlier = False, False
    if x < x_lower or x > x_upper:
        x_outlier = True
    if y < y_lower or y > y_upper:
        y_outlier = True
    if x_outlier and y_outlier:
        return True
    return False

def remove_children(stat):
    if "children" in stat:
      return str(stat).split("children")[0][:-1] + "}"

def get_stat(id, index):
    query = 'SELECT ast FROM samples WHERE id="'+id+'"'
    mycursor.execute(query)
    result = mycursor.fetchone()
    ast = result[0]
    as_dic = json.loads(ast)
    return str(as_dic[index])

def get_upper_lower(prob_key):
    result = get_samples(prob_key)
    all_points = []
    for code_tup in result:
        id = str(code_tup[0])
        # print("ID = ", id)
        dw = code_tup[1]
        if dw is not None:
            X = parse_data(dw)
            X_embedded = TSNE(n_components=2).fit_transform(X)
            for point in X_embedded:
                all_points.append(point.tolist())
    return quantiles(all_points)

def visualize_samples(prob_key):
    result = get_samples(prob_key)
    figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    f.write(str(prob_key)+"\n")
    for code_tup in result:
        id = str(code_tup[0])
        dw = code_tup[1]
        is_high_perf = str(code_tup[2])
        if dw is not None:
            X = parse_data(dw)
            X_embedded = TSNE(n_components=2).fit_transform(X)
            index = 0
            for point in X_embedded:
                point_col = "green"
                mark = 'o'
                if is_high_perf == "0":
                    point_col="red"
                is_outlier = check_outlier_2D(prob_key, point)
                if is_outlier is True:
                    statement = get_stat(id, index)
                    f.write(id+":"+statement+'\n')
                    mark = "x"
                    #plt.annotate(statement,
                    #             (point[0], point[1]),  # this is the point to label
                    #             textcoords="offset points",  # how to position the text
                    #             xytext=(0, 10),  # distance from text to points (x,y)
                    #             ha='right')
                plt.scatter(point[0], point[1], marker=mark, color=point_col)
                index += 1
    plt.savefig(prob_key+".png")

def predict_samples(prob_key):
    result = get_samples(prob_key)
    for code_tup in result:
        id = str(code_tup[0])
        dw = code_tup[1]
        is_high_perf = int(code_tup[2])
        if dw is not None:
            X = parse_data(dw)
            for vec in X:
                np.append(X, vec)
                np.append(y, is_high_perf)

select_problems()
#data_tuples = list(zip(X, y))
#df = pd.DataFrame(data_tuples)
#print(df.head())
#X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2)
#clf = svm.SVC()
#clf.fit(X_train, y_train)
#result = clf.predict(X_test)
print(result)
print(y_test)
