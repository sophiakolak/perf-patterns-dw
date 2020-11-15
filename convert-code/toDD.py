import mysql.connector
import json
import os

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)
mycursor = mydb.cursor(buffered=True)

'''
Gets serialized AST samples from database 'AST' field (samples table) 
Converts to data dependency graphs 
Adds data dependency (DD) graphs code to database 'DDgraph' field (samples table)
'''

def get_samples():
    query = 'SELECT id, AST FROM samples'
    mycursor.execute(query)
    return mycursor.fetchall()

def update_db(id, data):
    command = "UPDATE samples SET DDgraph=%s WHERE id=%s "
    values = (data, id)
    try:
        mycursor.execute(command, values)
        mydb.commit()
    except:
        print(id)

def write_list(edge_list, id):
    f = open(id + '.adjlist', 'w+')
    for edge in edge_list:
        f.write(edge + '\n')
    f.close()

def read_and_update(id):
    f = open(id+ '.adjlist',"r+")
    data = f.read()
    update_db(id,data)
    f.close()

def delete_files(id):
    os.remove(id+ '.adjlist')

def to_adj_list(ast, id):
    if ast == "":
        return
    else:
        i = 0
        edge_list = []
        as_dic = json.loads(ast)
        for dic in as_dic:
            edge = str(i)
            if "children" in dic:
                for y in dic["children"]:
                    edge += ' ' + str(y)
            edge_list.append(edge)
            i += 1
    print("-------------", id, "-----------")
    return edge_list

def make_dd_graph(ast, id):
    edge_list = to_adj_list(ast,id)
    if edge_list is None:
        return
    write_list(edge_list,id)
    read_and_update(id)
    delete_files(id)

def process_samples():
    result = get_samples()
    for code_tup in result:
        id = str(code_tup[0])
        ast = code_tup[1]
        make_dd_graph(ast,id)

process_samples()