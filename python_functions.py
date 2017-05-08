#Response object
import json
import os
from random import *
from db_models import db, User
import string
class Response():
	def __init__(self):
		self.code = 200
		self.msg = "OK"
		self.content = ""
		self.response_codes = {
		200:"OK",
		400:"Unknown client error",
		401:"Bad login",
		402:"Missing file",
		403:"File not allowed",
		404:"File extension not allowed",
		405:"Missing arguments in call",
		406:"Bad session token",
		411:"Bad accessToken",
		406:"Missing accessToken",
		407:"User not unique",
		500:"Unknown server error",
		501:"Method not allowed",
		502:"Unable to save file"
		}
	def status(self, new_value=False, content=False):
		if new_value:#new value should never be 0
			self.code = new_value
			self.msg = self.response_codes[self.code]
			self.content = content
		else:
			content = None
		return json.dumps({"response_code":self.code, "msg":self.msg, "content":self.content}, indent=4)

	def status_codes(self):
		return json.dumps(self.response_codes)

#Check if the filename is a typical image filename
def allowed_file(filename):
	allowed_extensions = set(["png", "jpg"])
	if filename.split(".")[1].lower() in allowed_extensions:
		return "." in filename
	return False

#Check wether the user already uploaded that image
def unique_image(image_url):
	image = open(image_url,"rb").read()
	if image == open(compare_image,"rb").read():
		pass

#Assert folder creation
def create_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
    	try:
    		os.makedirs(directory)
    	except:
        	return False
    return True

#Get images
def image_urls(token):
	os.listdir(token) # returns list

def new_token():
	chars = string.digits + string.ascii_uppercase
	length = 4
	token = ""
	for i in range(length):
		token += (choice(chars))
	return token

#DB Functions
def init_db():
	User.drop_table()
	db.create_tables([User])
	db.connect()

def register_user(email, password):
	token = new_token()
	User.create(email=email, password=password, token=token)
	return token

def unique_email(email):
	try:
		db_user = User.get(User.email == email)
	#Could not find any user
	except:
		return True
	return db_user.email != email

#Check accessToken
def valid_token(token):
	#This function checks if the user is logged in
	#Should fetch the tokens from a DB
	try:
		db_user = User.get(User.token == token)
	#Bad token
	except:
		return False
	return db_user.token == token