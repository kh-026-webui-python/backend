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
## Backend run server
```
python manage.py runserver
```

## Database

## Setup Postgresql
```
sudo apt install postgresql postgresql-contrib
sudo -u postgres psql
```
input into postgres=#
```
create user soft_user with password 'password';
create database soft_db;
grant all privileges on database soft_db to soft_user;
./manage.py migrate
```