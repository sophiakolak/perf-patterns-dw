import tokenize
from io import BytesIO
import keyword
import re
import mysql.connector
import os

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd=os.environ['mysql_pass'],
        database="leetcode"
)
mycursor = mydb.cursor(buffered=True)


def python_code_tokenize(full_code_text):
    '''
    :param full_code_text:
    :return:
    '''
    g = tokenize.tokenize(BytesIO(full_code_text.encode('utf-8')).readline)
    tokens = []
    prev_token = None
    try:
        for x in g:
            if x.type == tokenize.ENDMARKER:  # End Marker
                continue
            # if x.type == tokenize.COMMENT:
            #     continue
            elif x.type == tokenize.NEWLINE:
                tokens.append('NEW_LINE')
            elif x.type == tokenize.INDENT:
                tokens.append('INDENT')
            elif x.type == tokenize.DEDENT:
                tokens.append('DEDENT')
            elif x.type == tokenize.STRING:  # String
                s = x.string.strip()
                if s.startswith('"""') or s.startswith("'''"):
                    if prev_token is not None and (prev_token == '=' or prev_token == '(' or prev_token == ','):
                        tokens.append(x.string)
                    continue
                tokens.append(x.string)
                pass
            elif x.string == '\n':
                continue
            elif x.type < 57:
                tokens.append(x.string)
            prev_token = x.string.strip()
    except:
        raise
        pass
    code = " ".join(tokens)
    code = re.sub('[ \n\t]+', ' ', code)
    return code

query = 'SELECT array_key, runtime, is_high_perf, code FROM samples'
mycursor.execute(query)
results = mycursor.fetchall()

code_file = open("code.txt", "w+")
label_file = open("label.txt", "w+")
time_file = open("time.txt", "w+")
id_file = open("id.txt", "w+")

for res in results:
    prob_num = res[0]
    runtime = res[1]
    is_high_perf = res[2]
    code = res[3]
    tok_code = python_code_tokenize(code)
    code_file.write(tok_code+"\n")
    label_file.write(str(is_high_perf)+"\n")
    time_file.write(str(runtime)+"\n")
    id_file.write(str(prob_num)+"\n")



