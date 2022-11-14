# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.14-slim-buster

ENV PORT=5000
EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# install dependencies for mysqlclient
RUN apt update -y
RUN apt install python3-dev default-libmysqlclient-dev build-essential -y

# Install pip requirements
RUN python -m pip install gunicorn
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 4 --timeout 90 main:app
