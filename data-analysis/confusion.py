import seaborn as sns
import numpy as np

cf_matrix = np.array([[104257,2],[4446, 25186]])
print(cf_matrix)

group_names = ["True Neg","False Pos","False Neg","True Pos"]
group_counts = ["{0:0.0f}".format(value) for value in
                cf_matrix.flatten()]
group_percentages = ["{0:.2%}".format(value) for value in
                     cf_matrix.flatten()/np.sum(cf_matrix)]
labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in
          zip(group_names,group_counts,group_percentages)]
labels = np.asarray(labels).reshape(2,2)
hm = sns.heatmap(cf_matrix, annot=labels, fmt="", cmap='Blues')

#hm = sns.heatmap(cf_matrix/np.sum(cf_matrix), annot=True,
#            fmt='.2%', cmap='Blues')

fig = hm.get_figure()
fig.savefig('confusion.png')
