import os
from flask import *
from werkzeug.utils import secure_filename
from random import *
import json
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images"

#Response codes
response_codes = {
	200:"Successful",
	400:"Unknown client error",
	401:"Bad login",
	402:"Missing file",
	403:"File not allowed",
	404:"File extension not allowed",
	405:"Missing arguments in call",
	500:"Unknown server error",
	501:"Method not allowed",
	502:"Unable to save file"
	}

#Response object
class Response():
	def __init__(self):
		self.code = 200
	def status(self):
		return json.dumps([{"response_code":self.code, "content":response_codes[self.code]}], indent=4)

#register API
@app.route("/api/register", methods=["POST", "GET"])
def register_api():
	r = Response()
	if request.method == "POST":
		try:
			email = request.form["email"]
			password = request.form["password"]
			return r.status()
		except:
			r.code = 405
			return r.status()
	else:
		r.code = 501
		return r.status()


#Login for user to be able to start a session on the site
@app.route("/api/login", methods=["POST", "GET"])
def login_api():
	r = Response()
	if request.method == "POST":
		try:
			email = request.form["email"]
			password = request.form["password"]
		except:
			r.code = 405
			return r.status()

		if email == "root" and password == "root":
			#Return data from database, session token
			return r.status()
		else:
			r.code = 401
			return r.status()
	else:
		r.code = 501
		return r.status()

#File upload functions
#Check if the filename is a typical image filename
def allowed_file(filename):
	allowed_extensions = set(["png", "jpg"])
	if filename.split(".")[1].lower() in allowed_extensions:
		return "." in filename
	return False

#generate random name for files	
def random_name():
	return ''.join(choice(["1", "2", "3", "A", "B"]) for _ in range(6))

#Upload images api
@app.route("/api/upload", methods=["POST", "GET"])
def upload_api():
	r = Response()
	try:
		file = request.files["picture"]
	except:
		r.code = 405
		return r.status()
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
		    	r.code = 502
		    	return r.status()
		else:
			#File extension is not allowed
			r.code = 404
			return r.status()
	else:
		#File is missing
		r.code = 402
		return r.status()

#Show the responsecodes used under the api
@app.route("/api/codes", methods=["POST", "GET"])
def get_codes():
	return json.dumps([response_codes])


#Runs the app in dev mode
app.run(host="0.0.0.0", debug=True)