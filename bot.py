import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enables logging
import db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.environ['TOKEN']
ENV = os.environ['ENV']
PORT = int(os.environ.get('PORT', '8443'))
APP_NAME = os.environ['APP_NAME']


# We define command handlers. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Sends a message when the command /start is issued."""
    username = update.message.from_user.username
    update.message.reply_text('Hi ' + username + ' !')


def help(update, context):
    """Sends a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echos the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Logs Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Starts the bot."""

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # get requests from the bot
    if ENV == 'dev':
        # periodically connect to Telegram's servers to check for new updates
        updater.start_polling()
    elif ENV == 'prod':
        # transmit webhook URL to Telegram once. Telegram then sends update via the webhook
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()