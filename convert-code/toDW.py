import mysql.connector
import os

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)
mycursor = mydb.cursor(buffered=True)

'''
Gets data dependency graphs of samples from database 'DDgraph' field (samples table) 
Runs DeepWalk, stores embedding
Adds Embeddings to database 'deepwalk' field (samples table)
'''

def get_samples():
    query = 'SELECT id, DDgraph FROM samples'
    mycursor.execute(query)
    return mycursor.fetchall()

def update_db(id, data):
    command = "UPDATE samples SET deepwalk=%s WHERE id=%s "
    values = (data, id)
    try:
        mycursor.execute(command, values)
        mydb.commit()
    except:
        print(id)

def write_adjlist(graph,id):
    if graph is None:
        return
    f = open(id+'.adjlist', 'w+')
    f.write(graph)
    f.close()

def run_deepwalk(id):
    cmd = 'deepwalk --input ./' + id + '.adjlist --format adjlist --output ' + id + '.embeddings'
    try:
        os.system(cmd)
        f1 = open(id + '.embeddings', 'r')
        data = f1.read()
        f1.close()
        update_db(id,data)
    except:
        return

def delete_files(id):
    try:
        os.remove(id + '.adjlist')
        os.remove(id + '.embeddings')
    except:
        return

def make_embeddings(graph,id):
    write_adjlist(graph,id)
    run_deepwalk(id)
    delete_files(id)

def process_samples():
    result = get_samples()
    for code_tup in result:
        id = str(code_tup[0])
        graph = code_tup[1]
        make_embeddings(graph,id)

process_samples()