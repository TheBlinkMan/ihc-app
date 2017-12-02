FROM python:3.6-alpine

ENV FLASK_APP webapp.py
ENV FLASK_CONFIG production

RUN adduser -D ihcapp
USER ihcapp

WORKDIR /home/ihcapp

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY webapp.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
