import sqlite3
from peewee import *
db = SqliteDatabase("users.db")

class User(Model):
	email = CharField()
	password = CharField()
	token = CharField()
	class Meta:
		database = db
