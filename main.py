import logging
from config import TOKEN
from telegram import message, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
message_num = 0


def start(update, context):
    update.message.reply_text('Привет я бот для яндекс лицея!')


def help(update, context):
    update.message.reply_text('Помогите!')


def echo(update, context):
    global message_num
    update.message.reply_text(update.message.chat_id)
    message_num += 1


def msg_num(update, context):
    update.message.reply_text(str(message_num))


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("message_counter", msg_num))

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
