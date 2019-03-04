import json
import logging
import re
import requests
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token = os.environ['TELEGRAM_TOKEN']

updater = Updater(token=token)  # Токен API к Telegram
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

pattern_link = "https://crowdrepublic.ru/x/project/{}?mode=normal&scenario%5B%5D=finance&scenario%5B%5D=basic"
api_link = ""
project_id = ""


# Обработка текста
def text_message(bot, update):
    response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)


# Обработка команд
def start(bot, update):
    logger.warning("start")
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def set_link(bot, update):
    logging.warning("set")
    global api_link
    global pattern_link
    global project_id
    link_to_project = str(update.message.text)
    logging.warning(link_to_project)
    result = re.search('/project/(\\d*?)/', link_to_project)
    logging.warning(result.group(0))
    logging.warning(result.group(1))
    project_id = result.group(1)
    bot.send_message(chat_id=update.message.chat_id, text='Link setted to {}'.format(link_to_project))
    api_link = str(pattern_link).format(project_id)


def get_stat(bot, update):
    logging.warning("get_stat")
    project = get_json_project_from_crowd_api()
    title = project["title"]
    founded_sum = project["funded_sum"]
    near_goal = project["near_goal"]["target_sum"]
    bot.send_message(chat_id=update.message.chat_id,
                     text='Project: {0}. Current: {1}. Next goal: {2}'.format(title, founded_sum, near_goal))


def get_json_project_from_crowd_api():
    global api_link
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
    r = requests.get(api_link, headers=headers)
    result = re.match("<textarea>(.*)</textarea>", r.text)
    text = result.group(1)
    json_resp = json.loads(text)
    return json_resp["Project"]


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logger.warning("main")

    # Хендлеры
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, text_message))
    dispatcher.add_handler(CommandHandler('set', set_link))
    dispatcher.add_handler(CommandHandler('get_stat', get_stat))
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == '__main__':
    logger.warning("init")
    main()
