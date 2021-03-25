import logging
from config import TOKEN
from telegram import message, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyMarkup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Привет я бот для яндекс лицея!')


def help(update, context):
    update.message.reply_text('Help!')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def echo(update, context):
    keyboard = [
        [InlineKeyboardButton('text1', callback_data='button_callback_1')]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f'{update.message.chat.username} sayed: {update.message.text}',
                              reply_markup=markup)
    '''
    keyboard = [[KeyboardButton('text2')]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('text', reply_markup=markup)
    '''


def button(update: Update, context) -> None:
    query = update.callback_query
    print(query.data)
    query.answer()
    query.edit_message_text(text=f"Возврат кнопки: {query.data}")


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
