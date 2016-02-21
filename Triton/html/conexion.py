import sqlite3

conn = sqlite3.connect('triton.db')
c = conn.cursor()

#create table
c.execute('''Create Table User(email varchar(200), name var(100), last_name var(100))''') 

#insert data
c.execute("Insert into User values ('brianda_gdelatorre@outloo.com', 'brianda', 'Garcia')")

#sabe (commit) the changes

conn.commit()

#close session
conn.close()
