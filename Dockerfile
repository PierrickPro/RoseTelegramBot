FROM python:3.7

RUN pip3 install python-telegram-bot
RUN pip3 install requests
RUN pip3 install sqlalchemy
RUN pip3 install psycopg2
RUN pip3 install configparser
RUN pip3 install bech32

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/bot.py