# this is not related with the main code. just practice.
import sqlite3

conn = sqlite3.connect('mydatabase.db')

c = conn.cursor()

#c.execute("DROP TABLE IF EXISTS table_sample")
#c.execute("DELETE FROM table_sample")
c.execute("""CREATE TABLE IF NOT EXISTS table_sample (
          category text,
          name text,
          price integer )""")

c.execute("INSERT INTO table_sample VALUES ('category1','name1','50')")

c.execute("SELECT * FROM table_sample WHERE name='name1'")
c.execute("SELECT category FROM table_sample WHERE name='name1'")

print(c.fetchall())

conn.commit()
conn.close()