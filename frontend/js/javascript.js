function Request()
{
	this.url = "http://127.0.0.1:5000/api/";
	
	this.xhr = new XMLHttpRequest();
	this.response = null;//Until called
	
	//Parse received data
	this.parseData = function(data)
	{
		try
		{
			var parsedData = JSON.parse(data);
			console.log("Response:");
			console.log(parsedData);
			this.response = parsedData;
		}
		catch(e)
		{

			console.log("Could not parse!");
		}
		
	}

	//Get Request
	this.get = function(endpoint)
	{
		this.xhr.open("GET", this.url+endpoint, false);
		this.xhr.send(this.payload);
		
		var response = this.xhr.responseText;
		this.parseData(response);
	}

	//Post request
	this.post = function(endpoint)
	{
		this.xhr.open("POST", this.url+endpoint, false);
		this.xhr.send(this.payload.formData);
		
		var response = this.xhr.responseText;
		this.parseData(response);
	}
	
	//Used in almost all api calls, atleast for token
	this.Payload = function()
	{
		this.formData = new FormData();
		this.add = function(key, value)
		{
			this.formData.append(key, value)
		}
		this.remove = function(key)
		{
			this.formData.delete(key);
		}
		this.init = function(formId)
		{
			var form = document.getElementById(formId);
			this.formData = new FormData(form);
		}
	}
	//Data to send
	this.payload = new this.Payload();
}

//Copies the form at login.html and sends it
//Also handles the token
function login()
{
	request = new Request();
	formId = "loginForm";
	request.payload.init(formId);
	request.payload.add("token", "");
	request.post("login");
	if(request.response.response_code == 200)
	{
		saveToken(request.response.content);

		//Load home, no token needed
		window.location.href = "index.html";
	}
}

function logout()
{
	request = new Request();
	request.payload.add("token", token())
	request.post("logout");
	if(request.response.response_code == 200)
	{
		localStorage.token = 0;
		//Load login, no token needed
		window.location.href = "login.html";
	}
}


function register()
{
	request = new Request();
	formId = "registerForm";
	request.payload.init(formId);
	request.post("register");
	if(request.response.response_code == 200)
	{
		saveToken(request.response.content);

		//Redirect to login page
		window.location.href = "login.html";
	}
}

function autoLogin()
{
	token = localStorage.token;
	if(token != null)
	{
		if(token.length == 4)
		{
			request = new Request();
			request.payload.add("token", token);
			request.payload.add("email", "-");
			request.payload.add("password", "-");
			request.post("login");
			if(request.response.response_code == 200)
			{
				//Redirect to home page
				window.location.href = "index.html";
			}
		}
	}
}
function token()
{
	return localStorage.token;
}

function saveToken(token)
{
	localStorage.token = token;
}

function upload()
{
	request = new Request();
	request.payload.add("token", token());
	request.post("upload");
}