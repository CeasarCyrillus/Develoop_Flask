import sqlite3
def start():
	conn = sqlite3.connect("example.db")
	c = conn.cursor()
	c.execute('''CREATE TABLE users
	             (email TEXT, password TEXT)''')
	row = ("root", "root")
	c.execute("""INSERT INTO users VALUES (?, ?)""", row)
	conn.commit()
	conn.close()
def load():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	p = ('root',)
	c.execute('SELECT * FROM users WHERE password = ?', p)
	print(c.fetchone())
	conn.close()


