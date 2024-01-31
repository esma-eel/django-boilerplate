# pull official base image
FROM python:3.11.7

# set work dir
WORKDIR /usr/src/app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    netcat-traditional \
    libpq-dev \
&& rm -rf /var/lib/apt/list/*

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements/base.txt base.txt
# note: change this based on your environment
COPY ./requirements/production.txt requirements.txt
RUN pip install -r requirements.txt

# entrypoint
COPY ./entrypoint.production.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.production.sh
RUN chmod +x /usr/src/app/entrypoint.production.sh

# copy project
COPY . .

# run entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.production.sh"]