# Django Boilerplate Project README

## Overview

Django Boilerplate is a starter project template designed to kickstart development of Django applications quickly. It includes essential configurations, dependencies, and helpers to streamline the development process.

This project is just for starting an IDEA fast and dont think about authentication or basic django configurations.
I found Cookiecutter Django too complicated so I created this. 

- Django Version: 4.2.6
- Python Version: 3.11
- Coverage: 85%
- API Tests: Yes
- MTV Tests: No
- Tailwindcss version: 3.4.3
- Used Hyperui components
- Dockerized project with
    - https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

## How to Setup

### Prerequisites

- Ensure you have Python installed on your machine. The project supports Python 3.11
- Install Docker if you plan to use the Docker environment.


### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/esma-eel/django-boilerplate.git
   cd django-boilerplate
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
    For each environment, use the file corresponding to the same environment

   ```bash
   pip install -r requirements/local.txt
   ```

4. Start docker services for local development

    ```bash
    docker compose -f vsdebug.yml up -d --build
    ```
5. Environment variables
    - create a copy of envs_template in config and rename it as .envs
    - change .env.default values in your .envs for local development and vsdebug

6. Run migrations:

   ```bash
   python manage.py migrate
   ```

7. Create super user
    ```bash
    python manage.py createsuperuser
    ```

8. Collect static files (if applicable):

   ```bash
   python manage.py collectstatic --noinput --clear --no-post-process
   ```

9. Create api key (if appllicable):
    - Add API key for sms provider with code sms_provider_key
    - change communications.utils.sms to use another providers sdk (default is Kavenegar from Iran for test)

## Running Locally

To run the project locally, execute the following command:

```bash
python manage.py runserver 1337
```

The application will start on `http://127.0.0.1:1337/`.

In order to run the project locally along with vscode debugger use the following code for configuration of vscode debugger

```
{
    "name": "Python: Django",
    "type": "debugpy",
    "request": "launch",
    "program": "${workspaceFolder}/manage.py",
    "args": [
        "runserver",
        "1337"
    ],
    "console": "internalConsole",
    "django": true,
    "justMyCode": false,
},
```

## Running in Production

For deploying the project in a production production.yml file in your server to start services:

```bash
docker compose -f production.yml up -d --build
```


## MTV and Tailwindcss

### Install dependencies

Install dependencies with following command :

```bash
npm install package.json
```

### Running watcher

With following command tailwind will watch your HTML files and creates the css you can check package.json to see this command:

```bash
npm run watch:css
```


## Contributing

IDK how to do this yet.

## License

I did not choose one yet
but tell me if this project helped you
it will make me very happy
and help me fix my mistakes and get better
