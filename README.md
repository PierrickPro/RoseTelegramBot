# Rose Tracker Telegram Bot
[Project Video Demo](https://www.youtube.com/watch?v=712Hy_p8APk)

ROSE is a cryptocurrency token on the [Oasis Network](https://oasisprotocol.org) blockchain.</br>
I built a Telegram bot to track the details of your ROSE wallets.

## Deployment on Heroku using Docker

### Heroku Login
```
heroku login
```

### Create Database

```
heroku pg:psql --app rose-telegram-bot < wallet.sql
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
I wrote the commands in a shell script:
```
./deployment.sh
```

### Monitor Logs
```
heroku logs --app=rose-telegram-bot --tail
```
