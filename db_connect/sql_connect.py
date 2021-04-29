import sqlite3
from sqlite3 import Error

path = r'sql_db/my_db.db'
create_user = '''CREATE TABLE IF NOT EXISTS users (
					id integer PRIMARY KEY AUTOINCREMENT,
					user text NOT NULL,
					password text NOT NULL
					);'''

create_contacts = '''CREATE TABLE IF NOT EXISTS contacts (
					id integer PRIMARY KEY AUTOINCREMENT,
					name text NOT NULL,
					second_name text NOT NULL,
					email text NOT NULL,
					phone integer,
					FOREIGN KEY(user_id) REFERENCES users(user)
					);'''


def connect(path):
    '''Create a db connection to the SQLite database
            specified by the path
            :param path: database file
            :return: Connectin object or None
    '''
    connection = None
    try:
        connection = sqlite3.connect(path)
        print('Connection succesfull')
        return connection
    except Error as e:
        print(f'Error: {e}')


def close_connection(conn):
    '''Close given connection
    :param conn: Connection object
    :return: 
    '''
    try:
        conn.close()
        print('Connection was closed')
    except Error as e:
        print(f'Error: {e}')


def create_table(conn, query):
    '''create a table from the query statment
    :param conn: Connection object
    :param query: a CREATE TABLE statment
    :return:
    '''
    try:
        cursor = conn.cursor()
        cursor.execute('''PRAGMA foreign_keys=ON;''')
        cursor.execute(query)
    except Error as e:
        print(f'Error: {e}')


def create_user_contacts(conn):
    '''create database for user and contacts
    :param conn: Connectin object
    :return:
    '''
    create_table(conn, create_user)
    create_table(conn, create_contacts)


def do_query(conn, query, task):
    '''Execute query statment
    :param conn: Connection object
    :param query: query statment
    :return:
    '''
    cursor = conn.cursor()
    try:
        cursor.execute(query, task)
        conn.commit()
        print('Query succes!')
    except Error as e:
        print(f'Error: {e}')


def read_query(conn, query):
    '''Read query form data base
    :param conn: Connection object
    :param query: query statment
    :return result: data fetched from data base
    '''
    cursor = conn.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f'Error: {e}')
