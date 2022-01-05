# Rose Tracker Telegram Bot

## Deployment on Heroku using Docker

### Setup
```
heroku login
docker ps # make sure docker is running
```

### Default Deployment Commands
```
heroku container:login
heroku create
heroku container:push web
heroku container:release web
```

### Deploy From Apple Silicon
Deployment from Apple Silicon computers is slightly different.</br>
```
heroku container:login
docker buildx build --platform linux/amd64 -t rose-telegram-bot .
docker tag rose-telegram-bot registry.heroku.com/rose-telegram-bot/web 
docker push registry.heroku.com/rose-telegram-bot/web
heroku container:release web -a rose-telegram-bot
```
I wrote those commands in a shell script:
```
./deployment.sh
```

### Get Logs
```
heroku logs --app=rose-telegram-bot --tail
```
