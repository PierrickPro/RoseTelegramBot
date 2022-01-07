import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import parsemode
import bech32

import db
import oasis_scan_api

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.environ['TOKEN']
ENV = os.environ['ENV']
PORT = int(os.environ.get('PORT', '8443'))
APP_NAME = os.environ['APP_NAME']


def start(update, context):
    """Sends a message when the command /start is issued."""
    update.message.reply_text("Welcome to the Rose Telegram bot\n"
                              "If you need help, enter '/help'")


def help(update, context):
    """Sends a message when the command /help is issued."""
    help_message = '''How to use this bot:\n
Add a wallet: add myAddress myWalletName\n
Remove a wallet: remove myWalletName\n
Get details of all your wallets: wallets\n
Get details of one wallet: wallet myWalletName\n'''

    update.message.reply_text(help_message)


def reply(update, context):
    try:
        user_input = update.message.text
        words = user_input.split(' ')

        if words[0].lower() == 'add' and len(words) == 3:
            add_wallet(update, words)
        elif words[0].lower() == 'wallets' and len(words) == 1:
            get_wallets(update)
        elif words[0].lower() == 'wallet' and len(words) == 2:
            get_wallet(update, words)
        elif words[0].lower() == 'remove' and len(words) == 2:
            remove_wallet(update, words)
        else:
            update.message.reply_text('Invalid message, check /help')
    except Exception as e:
        logger.error(e)
        update.message.reply_text('Something went wrong...')


def add_wallet(update, words):
    # check if wallet has a valid format
    decoded_address = bech32.bech32_decode(words[1])

    if decoded_address[0] != 'oasis':
        update.message.reply_text('Invalid Wallet Address')
    else:
        db.insert_wallet(words[1], words[2], update.message.from_user.username)
        update.message.reply_text("Wallet added")


def remove_wallet(update, words):
    username = update.message.from_user.username

    if len(db.get_wallet(username, words[1])) == 0:
        update.message.reply_text("Wallet \"{0}\" doesn't exist".format(words[1]))
    else:
        db.delete_wallet(username, words[1])
        update.message.reply_text("Wallet removed")


def get_wallets(update):
    username = update.message.from_user.username

    wallets = db.get_wallets(username)

    for wallet in wallets:
        reply_message = oasis_scan_api.get_wallet_info(wallet['address'])
        update.message.reply_text(wallet['name'] + ':\n' + reply_message, parse_mode=parsemode.ParseMode.HTML)

    if len(wallets) == 0:
        update.message.reply_text("No wallet found")


def get_wallet(update, words):
    username = update.message.from_user.username

    wallets = db.get_wallet(username, words[1])

    for wallet in wallets:
        reply_message = oasis_scan_api.get_wallet_info(wallet['address'])
        update.message.reply_text(wallet['name'] + ':\n' + reply_message, parse_mode=parsemode.ParseMode.HTML)

    if len(wallets) == 0:
        update.message.reply_text("No wallet found")


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
    dp.add_handler(MessageHandler(Filters.text, reply))

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
