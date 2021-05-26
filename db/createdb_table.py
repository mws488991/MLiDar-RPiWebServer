import sqlite3
import sys

conn = sqlite3.connect('malidarData.db')

with conn:
    cr = conn.cursor()
    cr.execute("CREATE TABLE mlidar_data(dateOder DATE,trackNo TEXT,weight INTEGER,width INTEGER,height INTEGER,length INTEGER,sender TEXT, addressee TEXT)")