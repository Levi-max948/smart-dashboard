import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host = 'mysql.railway.internal',
        user = 'root',
        password = 'AXeQsChaHQLKOULWqFktPdYGArdBRnwc',
        database = 'railway'
    )
