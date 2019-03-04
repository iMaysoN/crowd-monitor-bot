import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from Handlers import *

# Входные точки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.warning("launch")

    bot = Updater(token=os.environ['TELEGRAM_TOKEN'])  # Токен API к Telegram
    dispatcher = bot.dispatcher

    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message))
    dispatcher.add_handler(CommandHandler('set', set_link))
    dispatcher.add_handler(CommandHandler('get_info', get_info))
    dispatcher.add_handler(CommandHandler('help', help))
    # Начинаем поиск обновлений
    bot.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    bot.idle()


if __name__ == '__main__':
    main()
