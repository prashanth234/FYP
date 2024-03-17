# FYP

## Getting Started Project Setup

#### Git Download 

https://git-scm.com/downloads

#### Generate the ssh keys and add to the github account using below link

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

#### Download VS Code

https://code.visualstudio.com/Download

#### Clone the repository 

git clone git@github.com:prashanth234/FYP.git


#### Download mysql community server 8.x

MacOS

Install mysql using homebrew

START SERVICE - brew services start mysql

ADD PASSWORD FOR ROOT - mysql_secure_installation

Windows

https://dev.mysql.com/downloads/windows/installer/8.0.html

Give password as root for the root user during installation.

#### Run the sql query

CREATE SCHEMA `fyp` ; 

#### Download mysql community workbench any version (It comes windows msi installer)

https://dev.mysql.com/downloads/workbench/

#### Install python 3.10

https://www.python.org/downloads/

windows - check the box add to path while installation

check version - python --version

https://www.python.org/downloads/macos/ (Download the macOS 64-bit universal2 installer)

#### Install pipenv to control the virtual environments 

pip3 install pipenv

#### Install the packages specified in pipfile.lock

pipenv install or pipenv install --dev (if there are dev dependencies) should be ran. That will install all the dependencies in the Pipfile
if the virtualenv is already activated, you can also use pipenv sync or pipenv sync --dev for the same effect
cd backend
pipenv sync

#### ACTIVATE VIRTUAL ENV

pipenv shell

#### Now migration the tables to sql

python manage.py migrate

#### Run the backend server

python manage.py runserver

#### To generate a sceret key

echo "$(openssl rand -hex 40)"

#### Download nvm to manage nodejs version or you can directly install nodejs 18.16.0

https://github.com/coreybutler/nvm-windows

nvm install 18.16.0

nvm use 18.16.0

check version - node --version

Download installer for mac
https://nodejs.org/en/download

#### Setup frontend

#### diable builtin typescript in vs code

https://vuejs.org/guide/typescript/overview.html#volar-takeover-mode

#### Install ionic cli (7.0.1)
npm i -g @ionic/cli

ionic --version

cd frontend

npm i

ionic serve

ionic serve --external (To bind to 0.0.0.0 which allows you to access from mobile)

python manage.py runserver 0.0.0.0:8000

#### ********** Application has been setup ********** 

 http://localhost:8100


#### Automation Tests 

- Add graphl/(slash) in fyp/urls.py
- pipenv run pytest

#### Performance Tests

pipenv run locust -f locustfiles/browse_categories.py

#### To generate full schema

pipenv run python manage.py graphql_schema --schema fyp.schema.schema --out schema.json
pipenv run python manage.py graphql_schema --schema fyp.schema.schema --out schema.graphql

#### Intial Data Setup

Dump data - python manage.py dumpdata categories.post > ./initial_data/post_data.json

Ensure that first user is product user

pipenv shell
python manage.py loaddata ./initial_data/category_data.json
python manage.py loaddata ./initial_data/competitions_data.json
python manage.py loaddata ./initial_data/post_data.json
python manage.py loaddata ./initial_data/postfile_data.json
python manage.py loaddata ./initial_data/reward_data.json
python manage.py loaddata ./initial_data/faq_data.json

Replace the original media folder

#### TROUBLESHOOT

Problem
[pipenv.exceptions.ResolutionFailure]: Warning: Your dependencies could not be resolved. You likely have a mismatch in your sub-dependencies.
  You can use $ pipenv run pip install <requirement_name> to bypass this mechanism, then run $ pipenv graph to inspect the versions actually installed in the virtualenv.
  Hint: try $ pipenv lock --pre if it is a pre-release dependency.
ERROR: Getting requirements to build wheel exited with 1

Solution
https://stackoverflow.com/questions/57461123/failed-to-build-mysqlclient-wheel-cannot-build-pip-install-mysqlclient-not-wor
pipenv install mysqlclient==2.1.0
(install mysqlclient version one that is before the python wheel package)

ERROR
pipenv not found

Solution
sudo -H pip install -U pipenv
PATH="$PATH:/Library/Frameworks/Python.framework/Versions/3.10/bin"

To Get Public IP
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` \
&& curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/public-ipv4