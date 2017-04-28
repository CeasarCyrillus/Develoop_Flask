import os
from flask import *
from werkzeug.utils import secure_filename
from random import *
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images"
#register API
@app.route("/api/register", methods=["POST"])
def register_api():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		#Database stuff should replace this nonsense
		#Here is also a good place to place email
		#check to confirm
		return "userToken"

#Login for user to be able to start a session on the site
@app.route("/api/login", methods=["POST"])
def login_api():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		if email == "root" and password == "root":
			return "userToken"#Return data from database, userToken
	return "101" #Bad login

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
@app.route("/api/upload", methods=["POST"])
def upload_api():
	file = request.files["picture"]
    # Check if the file is one of the allowed types/extensions

	if file and allowed_file(file.filename):
		# Make the filename safe, remove unsupported chars
	    filename = secure_filename(file.filename)

	    #Remember the pictures extension
	    file_ext = filename.split(".")[1]

	    #Save the file
	    try:
	    	new_filename = random_name() + "." + file_ext
	    	file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
	    except:
	    	return "202"#Could not upload file
	else:
			return "201" #Not allowed

	return "100" #Uploaded file correctly

#Runs the app in dev mode
app.run(host="0.0.0.0", debug=True)