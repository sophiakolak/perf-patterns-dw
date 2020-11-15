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
Gets Python2 samples from database 'py2code' field (samples table) 
Converts to serialized AST
Adds to database under 'AST' field (samples table)
'''
def update_db(id, data):
    command = "UPDATE samples SET AST=%s WHERE id=%s "
    values = (data, id)
    try:
        mycursor.execute(command, values)
        mydb.commit()
    except:
        print(id)

def get_samples():
    query = 'SELECT id, py2code FROM samples'
    mycursor.execute(query)
    return mycursor.fetchall()

result = get_samples()

def write_code(code,id):
    f = open(id + '_in.py', 'w+')
    f.write(code)
    f.close()

def read_and_update(id):
    f = open(id + '_out.txt', 'r+')
    data = f.read()
    update_db(id, data)
    f.close()

def build_ast(id):
    myCmd = 'python2 parse_python.py '+id+'_in.py > '+id+'_out.txt'
    os.system(myCmd)

def delete_files(id):
   os.remove(id+'_in.py')
   os.remove(id+'_out.txt')

def make_ast(code,id):
    write_code(code, id)
    build_ast(id)
    read_and_update(id)
    delete_files(id)

def process_samples():
    result = get_samples()
    for code_tup in result:
        id = str(code_tup[0])
        code = code_tup[1]
        make_ast(code,id)

process_samples()

