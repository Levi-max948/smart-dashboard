import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'king1manish',
        database = 'smart_dashboard'
    )