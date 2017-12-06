FROM python:3.6-alpine

ENV FLASK_APP webapp.py
ENV FLASK_CONFIG production
ENV MAIL_DEFAULT_SENDER "IHC APP <youremail@email_provider.com>"
ENV MAIL_USERNAME youremail@email_provider.com
ENV MAIL_PASSWORD yourpassword
ENV ADMIN_EMAIL admin_email@email_provider.com
ENV SECRET_KEY "put here the random secret key"

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
