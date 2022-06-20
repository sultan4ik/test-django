import logging
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, ConversationHandler, \
    CallbackQueryHandler, PrefixHandler

TOKEN = '5281798870:AAGsZxkOG7Dc1CvGYMER1JmWnRt3yjeDYqE'
telegram.constants.MESSAGEENTITY_ALL_TYPES
updater = Updater(token=TOKEN)  # получаем экземпляр 'Updater'
dispatcher = updater.dispatcher # получаем экземпляр 'Dispatcher'


def start(update, context):
    """Команда /start - стартовая"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я Тестовый бот")


def echo(update, context):
    """Функция обратного вызова - отправляет то, что принял"""
    text = 'Эхо: ' + update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def caps(update, context):
    """Команда /caps - отвечает верхним регистром"""
    if context.args:
        text_cups = ' '.join(context.args).upper()
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_cups)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='No command argument')
        context.bot.send_message(chat_id=update.effective_chat.id, text='send: /caps argument')


def inline_caps(update, context):
    """Режим встроенных запросов"""
    query = update.inlint_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(), title='Convert to UPPER TEXT', input_message_content=InputTextMessageContent(query.upper)
        )
    )
    context.bot.answer_inline_query(update.inlint_query.id, results)


def unknown(update, context):
    """Функция обрабатывает незнакомые команды"""
    context.bot.send_message(chat_id=update.effective_chat.id, text="Не знаю такой команды")


def callback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Это тестовая функция")


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO) # настройка логов

start_handler = CommandHandler('start', start) # предназначен для обработки команд
dispatcher.add_handler(start_handler) # добавление обработчика в `dispatcher`

# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo) # предназначен для обработки всех сообщений
# dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps) # обработчик команды caps
dispatcher.add_handler(caps_handler)

inline_caps_handler = InlineQueryHandler(inline_caps) # обработчик встроенных запросов
dispatcher.add_handler(inline_caps_handler)

unknown_handler = MessageHandler(Filters.command, unknown) # обработчик неизвестных команд
dispatcher.add_handler(unknown_handler)

prefix_handler = PrefixHandler(['!', '#'], 'test', callback)
dispatcher.add_handler(prefix_handler)

# CallbackQueryHandler(callback) - для обработки запросов обратного вызова (нажатие кнопок встроенной клавиатуры)

# ConversationHandler(entry_points, states, fallbacks) - для ведения разговора с одним или несколькими пользователями
# через сообщения Telegram путем управления четырьмя коллекциями других обработчиков, где
# entry_points - список обработчиков сообщений, которые используются для инициирования разговора,
# state - представляет собой словарь dict, который в качестве ключей хранит состояния/этапы разговора, а в качестве
# значений этих ключей один или несколько связанных обработчиков сообщений, которые должны быть использованы, если
# пользователь отправляет сообщение, когда разговор с ними в настоящее время находится в этом состоянии/этапе,
# fallbacks - это список обработчиков сообщений, которые используются, если пользователь в данный момент находится в
# разговоре, но состояние либо не имеет связанного обработчика, либо обработчик, связанный с состоянием, не подходит
# для обновления, например, если обновление содержит команду, но ожидается обычное текстовое сообщение. Это поведение
# можно использовать для отмены разговора или сообщения пользователю, что его сообщение не было распознано.

# ChosenInlineResultHandler(callback) - для обработки обновлений Telegram, содержащих выбранный inline-результат.

# PollAnswerHandler(callback) - для обработки сообщений Telegram, содержащих ответ на опрос.

# PollHandler(callback) - для обработки сообщений Telegram, содержащих опрос

# PrefixHandler(prefix, command, callback) - для обработки пользовательских префиксных команд, начинающихся с префикса,
# отличного от '/'

# ChatMemberHandler - для обработки сообщений Telegram, содержащих обновления участников чата (покинул, присоединился)

# ShippingQueryHandler(callback) - для обработки запросов обратного вызова доставки Telegram, запускает функцию
# обратного вызова callback, если сообщение доставлено и прочитано

# PreCheckoutQueryHandler(callback) - для обработки запросов обратного вызова Telegram PreCheckout.

# TypeHandler() для обработки обновлений пользовательских типов. Тип type - тип сообщения, которые должен обрабатывать
# этот обработчик, как определено isinstance().

# StringRegexHandler(pattern, callback) предназначен для обработки обновлений строк на основе регулярного выражения,
# которое проверяет содержимое сообщения.

# StringCommandHandler(command, callback) предназначен для обработки строковых команд. Команды представляют собой
# сообщения, которые начинаются с /

updater.start_polling() # запуск прослушивания сообщений

updater.idle() # обработчик нажатия Ctrl+C для отключения бота