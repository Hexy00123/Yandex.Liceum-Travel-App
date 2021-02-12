import logging
import datetime as dt
from config import TOKEN
from telegram import message, Update
from telegram import ReplyKeyboardRemove
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Dispatcher, CallbackContext

# контроль ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
# --------------------------------Buttons-------------------------------------------------------------------------------
button_back_to_menu = 'В меню'
# __main menu__
button_help_1 = '🧾Расписание мероприятий'
button_help_2 = '📊FAQ - часто задаваемые вопросы'
button_help_3 = '📆Календарь'
button_help_4 = '🆘Помощь'
button_help_5 = '☎️Контакты'
button_help_6 = '🔦Интересности'
# __FAQ__
button_help_FAQ_live = '🛏Проживание'
button_help_FAQ_transfer = '🚌Трансфер'
button_help_FAQ_food = '🥕Питание'


# -----------------------Menu-------------------------------------------------------------------------------------------
# 🧾Расписание мероприятий
def button_help_handler_1(update: Update, context: CallbackContext):
    update.message.reply_text('Расписание мероприятий', reply_markup=ReplyKeyboardRemove())


# 📊FAQ -часто задаваемые вопросы
def button_help_handler_2(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=button_help_FAQ_live), KeyboardButton(text=button_help_FAQ_transfer)],
            [KeyboardButton(text=button_help_FAQ_food), KeyboardButton(text=button_back_to_menu)],
        ],
        resize_keyboard=True
    )
    update.message.reply_text(text='Здесь ты можешь найти ответы на часто задаваемые вопросы',
                              reply_markup=reply_markup)


def button_help_FAQ_live_handler(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=button_help_2), KeyboardButton(text=button_back_to_menu)]
        ]
    )
    update.message.reply_text(
        '''Размещение по 2 — 5 человек в светлых, просторных и чистых комнатах кампуса университета''',
        reply_keyboard=reply_markup)


def button_help_FAQ_food_handler(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=button_help_2), KeyboardButton(text=button_back_to_menu)]
        ]
    )
    update.message.reply_text(
        '''Сбалансированное 5-разовое питание, соответствующее СанПиН''', reply_keyboard=reply_markup)


def button_help_FAQ_transfer_handler(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        [
            [KeyboardButton(text=button_help_2), KeyboardButton(text=button_back_to_menu)]
        ]
    )
    update.message.reply_text(
        '''Обычно трансфер организовывается перед заездом, более подробную информацию вы можете узнать у организаторов''',
        reply_keyboard=reply_markup)


# 📆Календарь
def button_help_handler_3(update: Update, context: CallbackContext):
    update.message.reply_text('Календарь', reply_markup=ReplyKeyboardRemove())


# 🆘Помощь
def button_help_handler_4(update: Update, context: CallbackContext):
    update.message.reply_text('''Этот бот созданный для того, чтобы оповещать тебя о новых мероприятиях в Университете Иннополис
''', reply_markup=ReplyKeyboardRemove())


# ☎️Контакты
def button_help_handler_5(update: Update, context: CallbackContext):
    update.message.reply_text('Контакты', reply_markup=ReplyKeyboardRemove())


# 🔦Интересности
def button_help_handler_6(update: Update, context: CallbackContext):
    update.message.reply_text('Интересности', reply_markup=ReplyKeyboardRemove())


# ---------------------------------------------Functions----------------------------------------------------------------
def start(update, context):
    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('''Пока что в боте не много команд, но вот некоторые из них:
/keyboard - Открывает клавиатуру для полноценного пользования ботом
/close - убирает клавиатуру
/description - Описание бота''')


def message_handler(update, context):
    text = update.message.text
    # Menu
    if text == button_help_1:
        button_help_handler_1(update=update, context=context)
    elif text == button_help_2:
        button_help_handler_2(update=update, context=context)
    elif text == button_help_3:
        button_help_handler_3(update=update, context=context)
    elif text == button_help_4:
        button_help_handler_4(update=update, context=context)
    elif text == button_help_5:
        button_help_handler_5(update=update, context=context)
    elif text == button_help_6:
        button_help_handler_6(update=update, context=context)
    # FAQ
    elif text == button_help_FAQ_live:
        button_help_FAQ_live_handler(update=update, context=context)
    elif text == button_help_FAQ_food:
        button_help_FAQ_food_handler(update=update, context=context)
    elif text == button_help_FAQ_transfer:
        button_help_FAQ_transfer_handler(update=update, context=context)
    elif text == button_back_to_menu:
        keyboard(update=update, context=context)


def keyboard(update: Update, context: CallbackContext):
    reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=button_help_1), KeyboardButton(text=button_help_2)],
            [KeyboardButton(text=button_help_3), KeyboardButton(text=button_help_4)],
            [KeyboardButton(text=button_help_5), KeyboardButton(text=button_help_6)]
        ],
        resize_keyboard=True
    )
    update.message.reply_text(text='Ку, перед тобой открылось меню)', reply_markup=reply_markup)


def close(update: Update, context: CallbackContext):
    update.message.reply_text('Кнопки убраны.', reply_markup=ReplyKeyboardRemove())


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# ----------------------------------------------------------------------------------------------------------------------

def main():
    # бот+диспетчер
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # обработка сообщений
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('open', keyboard))
    dp.add_handler(CommandHandler('close', close))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    # ERRORS
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()  # ==while True


if __name__ == '__main__':
    main()
