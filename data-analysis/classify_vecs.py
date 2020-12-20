import mysql.connector
import os
from sklearn.metrics import confusion_matrix
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
import tokenize
from io import BytesIO
import keyword
import re
import mysql.connector
import os
from sklearn import svm

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)
mycursor = mydb.cursor(buffered=True)

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

X_list = []
query = "SELECT id, code, deepwalk, is_high_perf FROM samples"
mycursor.execute(query)
result = mycursor.fetchall()
for r in result:
    id = int(r[0])
    code = r[1]
    deepwalk = r[2]
    if deepwalk is None:
        continue
    is_high_perf = int(r[3])
    vecs = parse_data(deepwalk)
    for vec in vecs:
        vec.append(is_high_perf)
        X_list.append(vec)

X = np.asarray(X_list)
np.random.shuffle(X)
print(X.shape)
split_horizontally_idx = int(X.shape[0]* 0.8)
train = X[:split_horizontally_idx, :]
test = X[split_horizontally_idx:, :]
print(len(train))
print(len(test))

X_train, y_train = [],[]
for val in train:
    nums = val[:-1]
    label = val[-1]
    X_train.append(nums)
    y_train.append(label)

X_test, y_test = [],[]
for val in train:
    nums = val[:-1]
    label = val[-1]
    X_test.append(nums)
    y_test.append(label)

clf = svm.SVC()
clf.fit(X_train, y_train)

print("oh yeah, I guess I'm really Bimpson yeah")
index = 0
pred_labels = []
wrong = 0
for val in X_test:
    double_list = []
    double_list.append(val)
    pred_lab = clf.predict(double_list)
    pred_labels.append(pred_lab)
    true_lab = y_test[index]
    if pred_lab != true_lab:
        wrong += 1
    index += 1

tn, fp, fn, tp = confusion_matrix(y_test, pred_labels).ravel()
print("wrong percent", (wrong/len(y_test))*100)
print("true negative", tn)
print("true positive", tp)
print("false positive", fp)
print("false negative", fn)
print("total samples", len(y_test))

