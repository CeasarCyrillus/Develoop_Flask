from flask import *
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")
#Login for user to be able to start a session on the site
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		if request.form["password"] == "root":
			return "userToken"#Return data from database, userToken
	return "101" #Bad login

#Runs the app in dev mode
app.run(host="0.0.0.0", debug=True)