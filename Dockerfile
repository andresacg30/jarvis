# Jarvis
FROM python:slim as jarvis

ARG COMMIT_HASH

RUN useradd jarvis

WORKDIR /home/jarvis

COPY requirements.txt requirements.txt
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*
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

# Set a label for the commit hash
LABEL commit_hash=$COMMIT_HASH

ENTRYPOINT ["./boot.sh"]
