import sqlite3

def conectar():
    conn = sqlite3.connect("database/iim.db")
    return conn
