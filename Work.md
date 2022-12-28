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


# ############### ADD DEBUG TOOLBAR ##################
https://django-debug-toolbar.readthedocs.io/en/latest/installation.html


