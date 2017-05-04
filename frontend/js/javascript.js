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
function login()
{
	request = new Request();
	formId = "loginForm";
	request.payload.init(formId);
	request.post("login");
}