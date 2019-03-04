from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

token = "778249680:AAGdQFShvI2jxoWvs4HWq1uTpPkw9uCTIE8"

updater = Updater(token=token)  # Токен API к Telegram
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Обработка команд
def text_message(bot, update):
    response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)


def start(bot, update):
    logger.warning("start")
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logger.warning("main")

    # Хендлеры
    start_command_handler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, text_message)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == '__main__':
    logger.warning("init")
    main()