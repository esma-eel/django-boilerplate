FROM python:3.11.6-slim

WORKDIR .

COPY ./requirements/base.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./doker/celery/celery.Runner.sh /celery.Runner
RUN sed -i 's/\r$//g' /celery.Runner
RUN chmod +x /celery.Runner
