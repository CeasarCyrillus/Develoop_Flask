from flask import *
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

#Login for user to be able to start a session on the site
@app.route("/login_user", methods=["GET", "POST"])
def login_user():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		if email == "root" and password == "root":
			return "userToken"#Return data from database, userToken
	return "101" #Bad login

#Login page for user interaction
@app.route("/login")
def login_page():
	return render_template("login.html")

#form to register a user
@app.route("/register")
def register_page():
	return render_template("register.html")

@app.route("/register_user", methods=["POST"])
def register_user():
	if request.method == "POST":
		email = request.form["email"]
		password = request.form["password"]
		#Database stuff should replace this nonsense
		#Here is also a good place to place email
		#check to confirm
		return "userToken"
#Runs the app in dev mode
app.run(host="0.0.0.0", debug=True)