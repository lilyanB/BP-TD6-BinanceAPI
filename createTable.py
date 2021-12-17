import sqlite3
conn = sqlite3.connect('myDB.db')
cur = conn.cursor()
req = "create table ApiBinance20211210(Id integer primary key, date int, high real, low real, open real, close real, volume real)"
cur.execute(req)
conn.commit()
conn.close