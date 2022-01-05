heroku container:login
docker buildx build --platform linux/amd64 -t rose-telegram-bot .
docker tag rose-telegram-bot registry.heroku.com/rose-telegram-bot/web  
docker push registry.heroku.com/rose-telegram-bot/web
heroku container:release web -a rose-telegram-bot
heroku logs --app=rose-telegram-bot --tail

