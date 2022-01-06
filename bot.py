import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import parsemode

import db
import oasis_scan_api
import bech32

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.environ['TOKEN']
ENV = os.environ['ENV']
PORT = int(os.environ.get('PORT', '8443'))
APP_NAME = os.environ['APP_NAME']


def start(update, context):
    """Sends a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Sends a message when the command /help is issued."""
    update.message.reply_text('Help!')


def add_wallet(update, context):
    w = 'oasis1qrdx0n7lgheek24t24vejdks9uqmfldtmgdv7jzz'
    a = bech32.bech32_decode(w)

    if a[0] != 'oasis':
        update.message.reply_text('Invalid Address')
    else:
        # insert in db

    return


def get_info(update, context):
    username = update.message.from_user.username
    addresses = db.get_wallets(username)

    for address in addresses:
        reply_message = oasis_scan_api.get_wallet_info(address)
        update.message.reply_text(reply_message, parse_mode=parsemode.ParseMode.HTML)


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
    dp.add_handler(CommandHandler("info", get_info))

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
