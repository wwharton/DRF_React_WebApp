FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
COPY cron.tab /app/cron.tab
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y cron rsyslog vim
COPY . /app
RUN service rsyslog start
RUN service cron start
RUN crontab /app/cron.tab




# write a cron file in docker file, copy it into directory, add a run command to load and run the tab file into cron



