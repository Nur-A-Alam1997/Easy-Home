import sqlite3
conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE IF NOT EXISTS post_ad_table (id INTEGER PRIMARY KEY AUTOINCREMENT, address TEXT, housetype TEXT, description TEXT, \
                rentfee TEXT, contactinformation TEXT,division TEXT, district TEXT, area TEXT, username TEXT)')


conn.execute('CREATE TABLE IF NOT EXISTS registration_table (name TEXT, username TEXT, email TEXT, password TEXT, Mobile_no TEXT, address TEXT)')
conn.execute('CREATE TABLE IF NOT EXISTS fav_tab(id INTEGER, address TEXT, housetype TEXT,\
                description TEXT, rentfee TEXT, contactinformation TEXT, division TEXT, district TEXT, area TEXT, username TEXT)')
# conn.execute('Drop TABLE post_ad_table')
# conn.execute('Drop TABLE fav_tab')
# address,housetype,rentfee,id
# print ("Table created successfully")
cursor=conn.cursor()
# cursor.execute('DELETE FROM post_ad_table WHERE id=3 ')
# cursor.execute('UPDATE post_ad_table SET id=? where username = ? ',("1","arpohridx"))
conn.commit()
conn.close()
# with conn:
#     cursor=conn.cursor()
