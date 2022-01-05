FROM python:3.7

RUN pip3 install python-telegram-bot
RUN pip3 install requests

RUN mkdir /app
ADD . /app
WORKDIR /app

CMD python /app/bot.py