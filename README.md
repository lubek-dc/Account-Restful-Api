# Account-Restful-Api
![console](https://user-images.githubusercontent.com/32651459/123863495-f5767600-d929-11eb-92e1-1baf468b51e8.png)

## Main Features:
* SQLITE Database support
* Account system (Basic Authentication)

## Setup
* First you need to clone repo via: 

` git clone  --recursive https://github.com/lubek-dc/Account-Restful-Api.git `
* Then you need to create config.ini file in directory and type in

```ini
[SECURITY]
SECRET_KEY: Your Secret Key (Can be anything for example ThisIsSecret)
```

## Creating database 

* Open Repo in terminal or CMD

* create data base via:
    * `$ python` or `$ py `

    * `>> from app import db`

    * `>> db.create_all()`
### The last step is installing dependecies via: 

`
$ pip install -r requirments.txt 
(cmd must be opened in the repo folder too)
`

And u are done to start programming
# Dependencies:
## Main:
* flask https://github.com/pallets/flask
* flask_sqlalchemy https://github.com/pallets/flask-sqlalchemy
* flask_marshmallow https://github.com/marshmallow-code/flask-marshmallow
* werkzeug.security https://github.com/pallets/werkzeug
## Other:
* uuid
* jwt
* datetime
* functools
* configparser
