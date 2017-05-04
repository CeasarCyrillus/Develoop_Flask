import os
from flask import *
from werkzeug.utils import secure_filename
from random import *
import json
import os
from python_functions import *
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images"

#register API
@app.route("/api/register", methods=["POST"])
def register():
	r = Response()
	#Try and create starting folder for user
	if request.method == "POST":
		try:
			email = request.form["email"]
			password = request.form["password"]

			#Create token in DB with user
			token = register_user(email, password)
			return r.status(200, token)
		except:
			#Could not get arguments
			return r.status(405)
	else:
		#Method other than post not allowed
		return r.status(501)


#Login for user to be able to start a session on the site
@app.route("/api/login", methods=["POST"])
def login():
	r = Response()
	if request.method == "POST":
		try:
			email = request.form["email"]
			password = request.form["password"]
		except:
			#Could not get arguments in call
			return r.status(405)
		
		#Fetch token from DB
		user = User.select().where(User.email == email and User.password == password)
		#userToken should be fetched from a DB
		if user:
			return r.status(200, user[0].token)
		else:
			#Could not login user
			return r.status(401)
	else:
		#No other method than post is allowed
		return r.status(501)

#Upload images api
@app.route("/api/upload", methods=["POST"])
def upload():
	#Prepere response
	r = Response()

	#Try to fetch token and validate it
	try:
		token = request.form["token"]
		if not valid_token(token):
			#Accesstoken was denied
			return r.status(411)
	except:
		#Accesstoken is missing in call
		return r.status(406)
	
	#Try to get the file part
	try:
		file = request.files["picture"]
	except:
		#Missing file in call
		return r.status(402)
	
	#Check if file var is empty, and the file exist
	if file:
		if allowed_file(file.filename):
			# Make the filename safe,
			#remove unsupported chars
		    filename = secure_filename(file.filename)

		    #Remember the file extension
		    file_ext = filename.split(".")[1]

		    #Save the file
		    try:
		    	new_filename = random_name() + "." + file_ext
		    	file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
		    except:
		    	#Could not save file
		    	return r.status(502)
		else:
			#File extension is not allowed
			return r.status(404)
	else:
		#File is missing
		return r.status(402)

#Show the response-codes used under the api
@app.route("/api/codes", methods=["GET"])
def get_codes():
	r = Response()
	#No status codes needed
	return r.status_codes()

#Runs the app in dev mode
app.run(host="0.0.0.0", debug=True)