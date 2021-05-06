import sqlite3 as lite
from sqlite3 import Error
import os.path
import datetime

class Databaes_connect():
    def __init__(self):
        self.db_dir = "/home/pi/Desktop/MLiDar-RPiWebServer/db/malidarData.db"
        self.db_tablename = "mlidar_data"
        
    def create_connection(self):
        conn = None
        try:
            conn = lite.connect(self.db_dir)
            cur = conn.cursor()
            cur.execute('''SELECT * FROM mlidar_data''')
            conn.commit()
        except Error as e:
            print(e)
        return conn
    
    def display_table(self, conn):
        sql = ''' SELECT * FROM ''' + self.db_tablename
        cur = conn.cursor()
        
        for a_row in cur.execute(sql):
            
            print (a_row) 
        conn.commit()
        cur.close()
        return cur.lastrowid

    def insert_data(self, conn, task):
        sql = '''INSERT INTO mlidar_data(dateOder,trackNo,weight,width,height,length,sender,addressee) VALUES(?,?,?,?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, task)
        conn.commit()
        cur.close()
        return cur.lastrowid
    
    def delete_table(self, conn):
        sql = ''' DELETE FROM ''' + self.db_tablename
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        return cur.lastrowid
    
    #delete some data in table
    def delete_data(self, conn, track):
        
        cur = conn.cursor()
        sql = "DELETE FROM mlidar_data WHERE trackNo = '%s'" % track
        #print (sql)
        try:
            cur.execute(sql)
            conn.commit()
            print( 'Deleted')
        except:
            print('Not Delete ID ')
        return None
    
    def search_trackNo(self,conn, trackNo):
        sql = ''' SELECT * FROM ''' + self.db_tablename
        cur = conn.cursor()
        for a_row in cur.execute(sql):
             if a_row[1] == trackNo:
                 print(type(a_row[1]))
                 return a_row
        return None

    def list_table(self,conn):
        
        cur = conn.cursor()
        sql = "SELECT * FROM mlidar_data ORDER BY trackNo "
        #sql = sql.encode('utf-8')
        cur.execute(sql)
        rows = cur.fetchall()
        return rows
    
    def edit_data(self,conn,trackNo,sender,addressee):
        
        try:
            cur = conn.cursor()
            sql = "UPDATE mlidar_data SET sender='%s' , addressee='%s' WHERE trackNo ='%s' " % (sender, addressee, trackNo)
            print(sql)
            
            try:
                cur.execute(sql)
                conn.commit()
                print ('Edited') 
            except:
                print('Edit Error')
        except :
             print('Error')
        return None
             
    