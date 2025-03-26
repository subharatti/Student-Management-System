import sqlite3

conn = sqlite3.connect('markbook.db')  

cursor = conn.cursor()


cursor.execute("SELECT * FROM Tests")


setup_data = cursor.fetchall()


cursor.close()
conn.close()


for row in setup_data:
    print(row)

##cursor.execute("SELECT * FROM Students where id=1")
##
##
##setup_data = cursor.fetchall()
##
##
##cursor.close()
##conn.close()
##
##
##for row in setup_data:
##    print(row)
