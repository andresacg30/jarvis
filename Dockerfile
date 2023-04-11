# Jarvis
FROM python:3.10 as jarvis

RUN useradd jarvis

WORKDIR /home/jarvis

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install gunicorn pymysql cryptography

COPY app app
COPY migrations migrations
COPY jarvis.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP jarvis.py

RUN chown -R jarvis:jarvis ./
USER jarvis

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]
