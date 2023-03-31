from flask import Flask, request, jsonify 
import sqlite3
import psycopg2

app=Flask(__name__)

# def db_connection():
#     conn=None
#     try:
#         conn= sqlite3.connect('students.sqlite')
#     except sqlite3.error as e:
#         print(e)
#     return conn
 

# @app.route('/', methods=['GET','Post'])
# def student():
#     conn= db_connection()
#     cursor = conn.cursor()

#     if request.method =="GET":
#         cursor=conn.execute("SELECT * FROM book")
#         students=[
#             dict(id=row[0],Name=row[1],Department=row[2])
#             for row in cursor.fetchall()
#         ]
#         if students is not None:
#             return jsonify(students)
       
#     if request.method== "POST":
        
#         new_name = request.json['Name']
#         new_department = request.json['Department']

#         sql_query = """INSERT INTO book (Name, Department) 
#                        VALUES (?,?) """
#         cursor= cursor.execute(sql_query,(new_name,new_department))
#         conn.commit()

#         return "student created.",201
conn= psycopg2.connect(database="flask_db", 
                    user="postgres",
                    password=123456, 
                    host="localhost", port="5432")
cursor=conn.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS student (id serial \
#     PRIMARY KEY, name varchar(100), department varchar(100), anything integer);""")
cursor.execute("""CREATE TABLE IF NOT EXISTS student_table (id serial \
    PRIMARY KEY, name varchar(100), department varchar(100), anything integer);""")
# cursor.execute(
#     '''INSERT INTO student_table (name, department, anything) VALUES \
#     ('Fahim', 'CSE', 1232);''')
conn.commit()
cursor.close()
conn.close()


def db_connection():
    conn=None

    conn= psycopg2.connect(database="flask_db", 
                    user="postgres",
                    password=123456, 
                    host="localhost", port="5432")
    return conn

@app.route('/', methods=['GET','Post','PUT', 'DELETE'])
def student():
    conn= db_connection()
    cursor = conn.cursor()
    
    if request.method =="GET":
        cursor.execute("SELECT * FROM student_table")
        students=[
            dict(id=row[0],name=row[1],department=row[2], anything=row[3])
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()
        if students is not None:
            return jsonify(students)
        else:
            message = message=[dict(state=False,message="No Student Record")]
            return jsonify(message)
        
    
    if request.method== "POST":
        name = request.json['name']
        department= request.json['department']
        anything = request.json['anything']

        cursor.execute('''INSERT INTO student_table \
                        (name, department, anything) VALUES (%s, %s, %s)''',
                        (name, department, anything))
        conn.commit()
        cursor.close()
        conn.close()
        message=[dict(state=True,message="Student Record Created")]
        return jsonify(message)
    
    if request.method == "PUT":
        name = request.json['name']
        department= request.json['department']
        anything=request.json['anything']
        id = request.json['id']

        cursor.execute(
            '''UPDATE student_table SET name=%s,\
            department=%s, anything= %s WHERE id=%s''', (name, department, anything, id))
  
        conn.commit()
        cursor.close()
        conn.close()
        return "student updated"
    
    if request.method =="DELETE":
        id = request.json['id']

        cursor.execute('''DELETE FROM student_table WHERE id=%s''', (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return "student deleted"
    
