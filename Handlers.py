import json
import re

import requests

from Main import logger

project_id_pattern = re.compile('/project/(\\d*?)/')
crowd_api_pattern = re.compile('<textarea>(.*)</textarea>')
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}
blueprint_to_api_request_by_project_id = "https://crowdrepublic.ru/x/project/{}?mode=normal&scenario%5B%5D=finance&scenario%5B%5D=basic"

link_cache = dict()

help_message = "Добрый день. Я - вумный бот-красопендра!\nЧтобы установить ссылку на проект - используйте /set.\nДля " \
               "получения информации по установленному - /get\n Для помощи по каждой команде используйте help после " \
               "команды (например: /set help)"


# Обработка текста
def text_message(bot, update):
    # response = 'Получил Ваше сообщение: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=help_message)


# Обработка команд
def help(bot, update):
    logger.warning("help")
    bot.send_message(chat_id=update.message.chat_id, text=help_message)


def start(bot, update):
    logger.warning("start")
    bot.send_message(chat_id=update.message.chat_id, text='Привет! Это обычный пинг! Просто проверка связи.')


def set_link(bot, update):
    message_from_update = update.message.text
    logger.warning("/set {}".format(message_from_update))
    if 'help' in message_from_update:
        bot.send_message(chat_id=update.message.chat_id,
                         text='Команда /set <link> предназначена для установки ссылки '
                              'на проект на https://crowdrepublic.ru/ для '
                              'мониторинга. После установки проект привязывается к '
                              'данному чату и вся транслирующаяся информация будет '
                              'исключительно о нем. Но через /set всегда можно '
                              'переставить проект в любой момент.')
    else:
        result = re.search(project_id_pattern, message_from_update)
        api_request_link = str(blueprint_to_api_request_by_project_id).format(result.group(1))
        project = get_json_project_from_crowd_api(link_cache.get(update.message.chat_id))
        bot.send_message(chat_id=update.message.chat_id,
                         text='Проект: {0}\nТекущая сумма: {1}'.format(project["title"], project["funded_sum"]))
        logger.warning('Set with {0} link -> api link: {1}'.format(message_from_update, api_request_link))
        link_cache[update.message.chat_id] = api_request_link


def get_info(bot, update):
    message_from_update = update.message.text
    logger.warning("/get with {}".format(message_from_update))
    if 'help' in message_from_update:
        project_hint = ''
        if update.message.chat_id in link_cache:
            if not link_cache.get(update.message.chat_id):
                project_hint = '\nНа текущий момент установлен проект: {}'.format(
                    link_cache.get(update.message.chat_id))
        bot.send_message(chat_id=update.message.chat_id,
                         text='Команда /get_info для выведения текущий основной статистики проекта, сначала нужно '
                              'установить проект для слежения через /set <link>, а потом можно использовать эту '
                              'команду для получения статистики по ручному запросу.{}'.format(project_hint))
    else:
        project = get_json_project_from_crowd_api(link_cache.get(update.message.chat_id))
        title = project["title"]
        founded_sum = project["funded_sum"]
        near_goal = project["near_goal"]["target_sum"]
        bot.send_message(chat_id=update.message.chat_id,
                     text='Проект: {0}\nТекущая сумма: {1}\nБлижайшая цель: {2}'.format(title, founded_sum, near_goal))


# Ловим ошибки и репортим
def error(update, context):
    logger.error('Update "%s" caused error "%s"', update, context.error)


# Полезные обработчики
def get_json_project_from_crowd_api(link):
    r = requests.get(link, headers=headers)
    result = re.match(crowd_api_pattern, r.text)
    text = result.group(1)
    json_resp = json.loads(text)
    return json_resp["Project"]
