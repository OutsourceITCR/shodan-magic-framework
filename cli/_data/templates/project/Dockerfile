FROM python:3.9-slim

RUN apt-get -q -y update
RUN apt install -y git
WORKDIR /app

COPY requirements.txt .
COPY lib/magic_frame_py/cli/main.py /app/lib/magic_frame_py/cli/main.py

RUN pip install -q -r ./requirements.txt --quiet --no-cache-dir
RUN chmod +x /app/lib/magic_frame_py/cli/main.py
RUN ln -s /app/lib/magic_frame_py/cli/main.py /usr/bin/magicli

EXPOSE 4000