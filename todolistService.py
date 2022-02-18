import sqlite3
import random
import string
from datetime import date

class todolistService:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database) # auto create file if not exist.
        self.prepare_table()

    def exist_table(self):
        sql = """SELECT name FROM sqlite_master WHERE type='table' AND name='todo'"""
        c = self.conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        return False if rows == [] else True

    def prepare_table(self):
        if(self.exist_table() == False):
            try:
                sql = '''CREATE TABLE todo
                            (title text, status text, created_at text, updated_at text)'''
                c = self.conn.cursor()
                c.execute(sql)		
                self.conn.commit()
            except Exception as e:
                print(e)

    def generate_row(self, total):
        today = date.today()
        start = 0
        while start < total:
            chars = "".join( [random.choice(string.ascii_lowercase) for i in range(15)] )
            self.create_todo((chars, "pending", today, today))
            start += 1

    def get_todo(self, todo_id = None, filter = None):
        sql = '''SELECT rowid,* from todo'''
        if(todo_id != None or filter != None):
            sql = sql + ''' where '''
        if(todo_id != None):
            sql = sql + '''rowid = ''' + todo_id
        if(filter != None):
            sql = sql + '''title like "%''' + filter + '''%"'''
        c = self.conn.cursor()
        c.execute(sql)     
        rows = c.fetchall()
        return rows

    def create_todo(self, todo):
        sql = '''INSERT INTO todo(title,status,created_at,updated_at) VALUES(?,?,?,?)'''
        c = self.conn.cursor()
        c.execute(sql, todo)
        self.conn.commit()
        return c.lastrowid

    def update_todo(self, todo_id, todo):
        sql = '''UPDATE todo SET title = ?, status = ?, updated_at = ? where rowid = ''' + todo_id
        c = self.conn.cursor()
        c.execute(sql, todo)
        self.conn.commit()

    def delete_todo(self, todo_id):
        sql = '''DELETE from todo where rowid = ''' + todo_id
        c = self.conn.cursor()
        c.execute(sql)
        self.conn.commit()