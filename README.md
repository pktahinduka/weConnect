[![Build Status](https://travis-ci.org/pktahinduka/weConnect.svg?branch=master)](https://travis-ci.org/pktahinduka/weConnect)
[![Coverage Status](https://coveralls.io/repos/github/pktahinduka/shopeasy-flask-rest-api/badge.svg?branch=TravisCI-Test)](https://coveralls.io/github/pktahinduka/shopeasy-flask-rest-api?branch=TravisCI-Test)

# weConnect
weConnect is a platform that allows users to create and expose businesses to the world, while potential clients log in to view and review the businesses. weConnect is enriched with a Python backend and a ReactJS frontend as the view in the MVC model adapted for the project. It also uses Postgres Database for data storage and retrieval. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python3.6
* PostgreSQL

#### Installation

Please ensure that development libraries for [PostgreSQL](http://techarena51.com/index.php/flask-sqlalchemy-postgresql-tutorial/) are installed.

#### Step 1: Clone the project to your application folder.

    git clone https://github.com/pktahinduka/weConnect

#### Step 2: Install the requirements and add your Database configuration details.

    pip install -r requirements.txt

    vim config.py
    Fill in your database username, password, name, host etc

Clone the repo:

For HTTPS
```
$ git clone https://github.com/pktahinduka/weConnect.git
```


Change Directory into the project folder
```
$ cd weConnect
```

Create a virtual environment with Python 3.6
```
$ virtualenv --python=python3.6 [your_environment_name]
```

Activate the virtual environment you have just created
```
$ source your_environment_name/bin/activate
```

Install the application's dependencies from requirements.txt to the virtual environment
```
$ (your_environment_name) pip install -r requirements.txt
```

Create the database:
For Postgres
```
$ createdb users_dev
$ createdb users_test
```

For other databases modify the `project/config.py`

Migrations:
```
$ (your_environment_name) python manage.py db init
$ (your_environment_name) python manage.py db migrate
$ (your_environment_name) python manage.py db upgrade
```    
     
#### Step 3: Run the application 
     
     - python manage.py runserver

#### Step 4: Run tests for the routes and configurations
    
     - python manage.py test

#### Step 5: Run coverage for the routes and configurations
    
     - python manage.py cov


### Specifications for the weConnect API
```
ENDPOINT                                         FUNCTIONALITY                          PUBLIC ACCESS

POST    /auth/login                              Logs a user in                         TRUE
POST    /auth/register                           Register a user                        TRUE
POST    /businesses                              Create a new business                  FALSE
GET     /businesses                              List all the created businesses        FALSE
GET     /businesses/<biz_id>                     Get a single business                  FALSE 
PUT     /businesses/<biz_id>                     Update this business                   FALSE
DELETE  /businesses/<biz_id>                     Delete a particular business           FALSE
POST    /reviews                                 List all reviews about businesses      FALSE
POST    /users                                   Create a new user                      FALSE
GET     /users                                   Get all users                          FALSE
GET     /users/<user_id>                         Get a particular user                  FALSE
```


**Contributions are highly welcomed and appreciated**

## Libraries
[Flask](http://flask.pocoo.org/) - Flask is a microframework for Python based on Werkzeug, Jinja 2 and good intentions. 

[SQLAlchemy](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.


[SQLAlchemy]() - SQLAlchemy


## Authors

* **Peter Tahinduka**

## Acknowledgments

* Google Inc.
