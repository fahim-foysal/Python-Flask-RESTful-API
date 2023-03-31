import sqlite3


conn= sqlite3.connect("students.sqlite")

cursor= conn.cursor()
sql_query= """ CREATE TABLE book(
    Id integer PRIMARY KEY,
    Name text NOT NULL,
    Department text NOT NULL
)"""
cursor.execute(sql_query)