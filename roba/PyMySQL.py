import  MySQLdb as DBB
import sys

def DBConnection(host, db, username, password, query):
    try:
        db = DBB.connect(host, username ,password ,db)
        connection = db.cursor()
        connection.execute(query)
        
        for rows in connection.fetchall():
            print rows[0], rows[1]

    finally:
        if connection:
            connection.close()

def test():
    DBConnection("db4free.net","iveco46","iveco46","test46","select * from test order by uno asc")

