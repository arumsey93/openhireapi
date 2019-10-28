## Bangazon API

Built using Python, Django, and the Django REST Framework for serving data to the

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

* Computer
* Bash Terminal
* [Python 3](https://www.python.org/downloads/)
* [Pip](https://pip.pypa.io/en/stable/installing/)
* Text editor (Visual Studio Code)

### Installing

1. Clone down this repository and cd into it.
2. Once inside this repository, cd into `openhireapi` and open your VSCode here with
`code .`
1. Create your virtual environment
```
python -m venv OpenHireEnv
```
* Start virtual environment on Mac
```
source ./OpenHireEnv/bin/activate
```
* Start virtual environment on Windows
```
source ./OpenHireEnv/Scripts/activate
```
5. Run `cd ..` You should be in a directory containing `requirements.txt`
6. Install the app's dependencies:
```
pip install -r requirements.txt
```

* Fire up that server!
```
python manage.py runserver
```

# Testing in Postman

## Registration
The database requires an authorization token in the Headers to succesfully request data.
* First, generate an authorization token by making a *POST* to `/register`
* In the body of the request, copy and paste the following code so that it resembles the image below
```
{
	"username":"test",
	"first_name":"test",
	"last_name":"test",
	"email":"test@test",
	"address":"test",
	"city":"test",
	"phone_number":"test",
	"password":"test"
}
```

* After *POSTING*, a response containing a token key will be provided. Copy and paste the value of that token.

* Include a header with a key of "Authorization" with a value of "Token {paste-token-here}"

Now you may GET, POST, PUT, and DELETE to any of the following resources:
* /Profile
* /Job
* /Favorite

### Authors

* [Alex Rumsey](https://www.linkedin.com/in/arumsey/)