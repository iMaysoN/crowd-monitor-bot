import logging
from telegram.ext import Updater, CommandHandler

token = "778249680:AAGdQFShvI2jxoWvs4HWq1uTpPkw9uCTIE8"


def start(update, context):
    logger.warning("start")
    update.message.reply_text(text="I'm a bot, please talk to me!")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logger.warning("main")
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logger.warning("init")
    main()
