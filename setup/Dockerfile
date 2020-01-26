FROM python:3.7

ENV user=butler
RUN useradd --user-group --create-home --no-log-init --shell /bin/bash $user
WORKDIR /home/$user

RUN apt update
RUN apt install ffmpeg -y

COPY setup/requirements.txt /tmp/
COPY . /home/$user
RUN pip install --no-cache-dir -r /tmp/requirements.txt
USER $user
