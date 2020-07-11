import sqlite3 as sq 
from sqlite3 import Error

#create database connection where user and expense data will reside

def database_connection(db_file):

    conn = None

    try:
        conn = sq.connect(db_file)
    except Error as e:
        print(e)

    return conn