import CrowdRepublicApi as crApi
from Main import logger

chat_id_to_project_id = dict()
help_message = "Добрый день. Я - вумный бот-красопендра!\n" \
               "Чтобы установить ссылку на проект - используйте /set <ссылка>.\n" \
               "Для получения информации по установленному - /get_info\n" \
               "Для помощи по каждой команде используйте help после команды (например: /set help)"


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
    logger.warning("Получено {0}".format(message_from_update))
    chat_id = update.message.chat_id
    if 'help' in message_from_update or not message_from_update:
        bot.send_message(chat_id=chat_id,
                         text='Команда /set <ссылка> предназначена для установки ссылки '
                              'на проект на https://crowdrepublic.ru/ для '
                              'мониторинга. После установки проект привязывается к '
                              'данному чату и вся транслирующаяся информация будет '
                              'исключительно о нем. Но через /set всегда можно '
                              'переставить проект в любой момент.')
    elif 'https' not in message_from_update:
        bot.send_message(chat_id=chat_id,
                         text='Простите, но ссылка не кажется мне валидной, не могли бы вы проверить? Она должна '
                              'выглядеть примерно так: '
                              'https://crowdrepublic.ru/project/1017400/Mutanty-Tochka-otschyota')
    else:
        project_id = crApi.get_id_from_message_with_web_link(message_from_update)
        chat_id_to_project_id[chat_id] = project_id
        project = crApi.get_project_via_api_by_id(project_id)
        bot.send_message(chat_id=update.message.chat_id,
                         text='Установлен проект: {0}\nТекущая сумма: {1}'.format(project["title"],
                                                                                  project["funded_sum"]))
        logger.warning('{0} link -> project id: {1}'.format(message_from_update, project_id))


def get_info(bot, update):
    message_from_update = update.message.text
    logger.warning("Получено {0}".format(message_from_update))
    chat_id = update.message.chat_id
    if 'help' in message_from_update:
        project_hint = ''
        if update.message.chat_id in chat_id_to_project_id:
            if not chat_id_to_project_id.get(update.message.chat_id):
                project_hint = '\nНа текущий момент установлен проект: {}'.format(
                    chat_id_to_project_id.get(update.message.chat_id))
        bot.send_message(chat_id=chat_id,
                         text='Команда /get_info для выведения текущий основной статистики проекта, сначала нужно '
                              'установить проект для слежения через /set <ссылка>, а потом можно использовать эту '
                              'команду для получения статистики по ручному запросу.{}'.format(project_hint))
    elif update.message.chat_id not in chat_id_to_project_id:
        bot.send_message(chat_id=chat_id,
                         text='Пожалуйста задайте предварительно проект, который хотите отслеживать')
    else:
        project_id = chat_id_to_project_id.get(chat_id)
        project = crApi.get_project_via_api_by_id(project_id)
        title = project["title"]
        founded_sum = project["funded_sum"]
        near_goal = project["near_goal"]["target_sum"]
        bot.send_message(chat_id=chat_id,
                         text='Проект: {0}\n'
                              'Текущая сумма: {1}\n'
                              'Ближайшая цель: {2}'.format(title, founded_sum, near_goal))


# Ловим ошибки и репортим
# Позволяет не умирать приложению, если вдруг словилась ошибка
def error(update, context):
    logger.error('Update "%s" caused error "%s"', update, context.error)
