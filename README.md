# FYP Getting Started

# Git Download 

https://git-scm.com/downloads

# Generate the ssh keys and add to the github account using below link

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

# Download VS Code

https://code.visualstudio.com/Download

# Clone the repository 

git clone git@github.com:prashanth234/FYP.git


# Download mysql community server 8.x

MacOS

Install mysql using homebrew

START SERVICE - brew services start mysql

ADD PASSWORD FOR ROOT - mysql_secure_installation

Windows

https://dev.mysql.com/downloads/windows/installer/8.0.html

Give password as root for the root user during installation.

# Run the sql query

CREATE SCHEMA `fyp` ; 

# Download mysql community workbench any version (It comes windows msi installer)

https://dev.mysql.com/downloads/workbench/

# Install python 3.10

https://www.python.org/downloads/

windows - check the box add to path while installation

check version - python --version

# Install pipenv to control the virtual environments 

pip3 install pipenv

# Install the packages specified in pipfile.lock

pipenv install or pipenv install --dev (if there are dev dependencies) should be ran. That will install all the dependencies in the Pipfile
if the virtualenv is already activated, you can also use pipenv sync or pipenv sync --dev for the same effect
cd backend
pipenv sync

# ACTIVATE VIRTUAL ENV

pipenv shell

# Now migration the tables to sql

python manage.py migrate

# Run the backend server

python manage.py runserver

# Download nvm to manage nodejs version or you can directly install nodejs 18.16.0

https://github.com/coreybutler/nvm-windows

nvm install 18.16.0

nvm use 18.16.0

check version - node --version

# Setup frontend

# diable builtin typescript in vs code

https://vuejs.org/guide/typescript/overview.html#volar-takeover-mode

# Install ionic cli (7.0.1)
npm i -g @ionic/cli

ionic --version

cd frontend

npm i

ionic serve

# ########## Application has been setup ############

 http://localhost:8100

 ### django admin ###

user: root
password: root