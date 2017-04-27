import os
from flask import *
from werkzeug.utils import secure_filename
from random import *
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "images"
@app.route("/")
def home():
	return render_template("index.html")

#form to register a user
@app.route("/register")
def register():
	return render_template("register.html")

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

#Login page for user interaction
@app.route("/login")
def login():
	return render_template("login.html")

#File upload functions
#Check if the filename is a typical image filename
def allowed_file(filename):
	allowed_extensions = set(["pngg", "jpgg"])
	if filename.split(".")[1].lower() in allowed_extensions:
		return "." in filename
	return False

#generate random name for files	
def random_name():
	return ''.join(choice(["1", "2", "3", "A", "B"]) for _ in range(6))

#Upload images page
@app.route("/upload")
def upload():
	return render_template("upload.html")

#Upload images api
@app.route("/api/upload", methods=["POST"])
def upload_api():
	#Get a list of uploaded images
	error = False
	uploaded_files = request.files.getlist("pictures[]")
	for file in uploaded_files: #Iterate every file
	    # Check if the file is one of the allowed types/extensions
	    if file and allowed_file(file.filename):
	        # Make the filename safe, remove unsupported chars
	        filename = secure_filename(file.filename)

	        #Remember the pictures extension
	        file_ext = filename.split(".")[1]

	        #Save the file
	        try:
	        	file.save(os.path.join(app.config['UPLOAD_FOLDER'], random_name() + "." + file_ext))
	        except:
	        	error = "202"#Could not upload file
	    else:
	   		error = "201" #Not allowed
	if not error:
		return "100" #Uploaded file correctly
	return error #Error message

#Runs the app in dev mode
app.run(host="0.0.0.0", debug=True)