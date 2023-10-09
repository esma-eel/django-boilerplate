# How To ?

## Set project folder in virtualenvwrapper
to cd to project folder when using "workon envname" command
enter "setvirtualenvproject" in root

to add project to python path and use django-admin insteado f python manage.py
use add2virtualenv . 
note: "." is current folder of project

## Setup environment variables
if you use virtualenv else use only export command in global
or put the export command in .bashrc or .zshrc files

cd ~/.virtualenvs/$NAMEOFVENV/bin
vim postactivate
    export DJANGO_SETTINGS_MODULE=config.settings.local
    export SECRET_KEY="somestring"

vim postdeactivate
    unset DJANGO_SETTINGS_MODULE
    unset SECRET_KEY

## Run commands of management.py
if you set previous step
you only need to set settings in postactivate and unset it in postdeactivate
but if you did not want to use env variables use below command

python manage.py cmdname --settings=config.settings.local


## Create app
mkdir ./boilerplate/appname
django-admin startapp appname ./boilerplate/appname