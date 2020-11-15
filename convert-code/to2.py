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
Gets Python3 samples from database 'code' field (samples table) 
Converts to Python2 with 3to2 
Adds Python2 code to database 'py2code' field (samples table)
'''
def update_db(id, data):
    command = 'UPDATE samples SET py2code="'+data+'" WHERE id="'+id+'"'
    try:
        mycursor.execute(command)
    except:
        print(id)
    mydb.commit()

def get_samples():
    query = 'SELECT id, code FROM samples'
    mycursor.execute(query)
    return mycursor.fetchall()

def write_code(code,id):
    f = open(id + '.py', 'w+')
    f.write(code)
    f.close()

def read_and_update(id):
    f = open(id + '.py', 'r+')
    data = f.read()
    update_db(id, data)
    f.close()

def convert_code(id):
    command = '3to2 -w ' + id + '.py'
    os.system(command)

def delete_files(id):
    try:
        os.remove(id + '.py')
        os.remove(id + '.py' + '.bak')
    except:
        print(id)

def convert_3_to_2(code,id):
    write_code(code, id)
    convert_code(id)
    read_and_update(id)
    delete_files(id)

def process_samples():
    result = get_samples()
    for code_tup in result:
        id = str(code_tup[0])
        code = code_tup[1]
        convert_3_to_2(code,id)


process_samples()