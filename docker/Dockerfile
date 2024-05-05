FROM python:3.10

WORKDIR /scrapper

COPY ./bot ./bot
COPY ./config ./config
COPY ./scripts ./scripts
COPY ./scrap_handlers ./scrap_handlers

COPY requirements.txt .

COPY main.py .
COPY main_async.py .

RUN mkdir db
RUN mkdir log

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "main_async.py"]