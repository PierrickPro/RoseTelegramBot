# Rose Tracker Telegram Bot


##Database

create table
```
heroku pg:psql --app rose-telegram-bot < wallet.sql
```


##Deployment on Heroku using Docker



###Setup
```
heroku login
docker ps # make sure docker is running
```

###Default Deployment Commands
```
heroku container:login
heroku create
heroku container:push web
heroku container:release web
```

###M1 Deployment

I've written a shell script to quickly deploy from an Apple Silicon machines
```
./deployment.sh
```
commands:
```
heroku container:login
docker buildx build --platform linux/amd64 -t rose-telegram-bot .
docker tag rose-telegram-bot registry.heroku.com/rose-telegram-bot/web 
docker push registry.heroku.com/rose-telegram-bot/web
heroku container:release web -a rose-telegram-bot
```

###Get Logs
```
heroku logs --app=rose-telegram-bot --tail
```