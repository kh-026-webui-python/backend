# SoftTest

## Backend setup
```
$ pip install -r requirements.txt
```

## Backend run server
```
python manage.py runserver
```

## Database

## Setup Postgresql
```
sudo -u postgres psql
create user soft_user with password 'password';
create database soft_db;
grant all privileges on database soft_db to soft_user;
./manage.py migrate
```
