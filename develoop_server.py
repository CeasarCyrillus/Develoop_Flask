import os
from flask import *
from werkzeug.utils import secure_filename
from random import *
import json
import os
from python_functions import *
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images"

#Response codes
#response_codes = {
#	200:"OK",
#	400:"Unknown client error",
#	401:"Bad login",
#	402:"Missing file",
#	403:"File not allowed",
#	404:"File extension not allowed",
#	405:"Missing arguments in call",
#	500:"Unknown server error",
#	501:"Method not allowed",
#	502:"Unable to save file"
#	}

#register API
@app.route("/api/register", methods=["POST"])
def register():
	r = Response()
	#Try and create starting folder for user
	if request.method == "POST":
		try:
			email = request.form["email"]
			password = request.form["password"]
			token = "userToken"
			create_dir("/images/"+token)
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
			#Return data from database, session token
			#This is development evn. rubbish
			user_in_database = True #Testing purpuses
			if user_in_database:
				return r.status(200, "userToken")
		else:
			#Could not login user
			return r.status(401)
	else:
		#No other method than post is allowed
		return r.status(501)

#Upload images api
@app.route("/api/upload", methods=["PUT"])
def upload():
	r = Response()
	try:
		file = request.files["picture"]
		token = request.form["token"]
		if token != "userToken":
			#Bad login
			return r.status(401)
	except:
		#Missing file in call
		return r.status(402)
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
#Download the users images
@app.route("/api/images", methods="GET")
def get_images():
	r = Response()
	if request.form["token"] != "userToken":
		#Bad login
		return r.status(401)
	if token == "userToken":
		r.content = image_urls(token)
		return r.status()
#Show the response-codes used under the api
@app.route("/api/codes", methods=["GET"])
def get_codes():
	return json.dumps([response_codes])


#Runs the app in dev mode
app.run(host="0.0.0.0", debug=True)