# CREATE A VIRTUAL ENV NAMED PYTHON3
python3 -m venv python3

# ACTIVATE
source python3/Scripts/activate

# INSTALL DJANGO PACKAGE
python -m pip install Django

# DEACTIVATE
deactivate

# ######## OR ##########

# INSTALL PIPENV (DEPENDENCY MANAGEMENT TOOL INSIDE A VIRTUAL ENVIRONMENT)
pip3 install pipenv

# Adding packages to pipfile
use pipenv instead of pip to install and add package to pipfile

# Install the packages specified in pipfile.lock
pipenv sync

# INSTALL DJANGO (CREATES A VIRTUAL ENVIRONMENT AND INSTALLS DJANGO INSIDE IT)
pipenv install django

# TO ACTIVATE VIRTUAL ENV
pipenv shell

# RUN A COMMAND INSIDE VIRTUAL ENV
pipenv run

# DJANOGO VERSION
python -m django --version

# CREATE PROJECT
django-admin startproject fyp .

# RUN SERVER
python manage.py runserver 9000(Optional port number)

# GET PATH OF VIRTUAL ENV
pipenv --venv ; and append /bin/python

# SELECT INTERPRETOR PYTHON IN VSCOE
ctrl + p - add the path you got or select the existing

# TO ACTIVATE
ctrl + `

# ################## CREATING APPS ####################

python manage.py startapp playground

# pipenv install is used for installing packages into the pipenv virtual environment and updating your Pipfile and Pipfile.lock.

# ############### ADD DEBUG TOOLBAR ##################

# Toolbar appears for only html pages
https://django-debug-toolbar.readthedocs.io/en/latest/installation.html

# Install the django toolbar (Adds temporarily to pip packages if you again do pipenv sync this package will not be installed again)
python -m pip install django-debug-toolbar

# TO add to pipfile and lock it.
pipenv install django-debug-toolbar 

# Change the db config in settings.py
# Install the mysqlclient
pipenv install mysqlclient

# Added a playground model in playground/models.py

# Create migrations for the models
python manage.py makemigrations (appname optional)

# To apply models to db
python manage.py migrate

# Install rest framework (https://www.django-rest-framework.org/)
pipenv install djangorestframework

# Install djoser
# REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation
pipenv install -U djoser

# JWT Handler
pip install -U djangorestframework_simplejwt
(or)
pipenv install djangorestframework_simplejwt

# GraphQL
pipenv install graphene-django

# create super user
python manage.py createsuperuser

username: admin
password: admin
email: admin@admin.com

# Refer to this documentation for all the authentication methods
https://django-graphql-auth.readthedocs.io/en/latest/quickstart/