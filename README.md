[![Build Status](https://travis-ci.org/kh-026-webui-python/backend.svg?branch=setup-travis)](https://travis-ci.org/kh-026-webui-python/backend)

# SoftTest


## Creating virtual environment
```
python3 -m venv /path/to/new/virtual/environment
```

## Activating virtual environment
```
source <path to venv>/bin/activate
```

## Backend setup
```
$ pip install -r requirements.txt
```
https://github.com/kh-026-webui-python/backend/network/members

## Database

### Setup Postgresql
##### Install database:
```
sudo apt install postgresql postgresql-contrib
```
##### Enter interactive session:
```
sudo -u postgres psql
```
##### Create user and database:
```
CREATE DATABASE soft_db;
CREATE USER soft_user WITH PASSWORD 'password';
```
##### Give the rights of access to the database for user:
```
ALTER ROLE soft_user SET client_encoding TO 'utf8';
ALTER ROLE soft_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE soft_user SET timezone TO 'UTC';
ALTER USER soft_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE soft_db TO soft_user;
```
##### To exit the postgres console:
```
\q
```

## Backend run server
```
python manage.py runserver
```

## How to set up Pylint

#### How to get Pylint rcfile

```
pylint --generate-rcfile > path/to/your/resource/file
```

#### Settings for Pycharm

```
 File -> Settings -> Tools -> External Tools -> Add("+" signs)
```

```
Name: whatever you like
Program: path/to/your/pylint
Arguments: $FilePath$ --rcfile=path/to/your/rcfile
Working directory: $ProjectFileDir$
```

## How to set up Pytest

```
Settings -> Tools -> Python Intergrated Tools
```

```
Default test runner: pytest
```

```
Edit Configurations -> Add("+" signs) -> Python tests -> pytest
```

```
Target: path/to/your/tests
```