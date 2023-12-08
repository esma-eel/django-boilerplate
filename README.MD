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

add codes below to apps.py

    name = "boilerplate.appname"
    verbose_name = _("Appname")

    def ready(self):
        pass

## flusth expired tokens
python manage.py flushexpiredtokens


## run redis server
docker-compose -f dc-redis.yml up -d --build

## connect to a container
to go with root in a container
docker exec -it -u 0 redis_server sh 

to go with noraml user in a container
docker exec -it -u 1 redis_server sh

## celery 
./doker/celery/celery.Runner.sh
i did some works on celery but finally i had to run the sh above
to use it in localhost

# TODO:
- remember to use .env files for docker later
- later you should put execution files of celery run in docker-compose (just a reminder)

