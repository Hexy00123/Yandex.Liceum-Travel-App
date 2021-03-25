import requests
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler, CallbackQueryHandler

TOKEN = '1631758161:AAHMcZDHtklVyLQTShpa5yGCoxoLwytyasQ'
KEY = '5ae2e3f221c38a28845f05b611939fdf10b5f750f31efaf84a6fa7c0'

location_keyboard = KeyboardButton('Найти достопримечательности вблизи', request_location=True)
custom_keyboard = [[location_keyboard]]
REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(custom_keyboard)

TITLES = {'callback_button1_adress': 'Адрес', 'callback_button2_map': 'Показать на карте'}
INDIFICATORS = ['callback_button1_adress', 'callback_button2_map']

KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton(TITLES[INDIFICATORS[0]], callback_data=INDIFICATORS[0]),
     InlineKeyboardButton(TITLES[INDIFICATORS[1]], callback_data=INDIFICATORS[1])
     ]])

site = 'https://geocode-maps.yandex.ru/1.x/?'
site2 = 'http://api.opentripmap.com/0.1/ru/places/xid/'
site3 = 'https://geocode-maps.yandex.ru/1.x/?'
site4 = 'https://static-maps.yandex.ru/1.x/?'
site5 = 'http://api.opentripmap.com/0.1/ru/places/radius?'

atractions = {}
position = []
pos = []

bot = Bot(TOKEN)


def location(update: Update, context):
    update.message.reply_text(str(update.message.location))
    position.append(str(update.message.location['longitude']))
    position.append(str(update.message.location['latitude']))


def start(update, context):
    update.message.reply_text('меню', reply_markup=REPLY_KEYBOARD_MARKUP)


def button_handler_attractions(update: Update, context):
    data = update.callback_query.data
    p = ', '.join(list(map(str, atractions[update.callback_query.message['text']])))
    req = requests.get(site, params={
        'geocode': p,
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
        'format': 'json',
        'kind': 'house'
    })
    point = update.callback_query.message['text']
    if data == INDIFICATORS[0]:
        bot.send_message(str(update.effective_chat['id']), text=
        req.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
            'GeocoderMetaData']['text'])
    if data == INDIFICATORS[1]:
        create_map(update, context, point)


def create_map(update: Update, context, point):
    params = f'll={",".join(position)}&l=map&pt={",".join(list(map(str, atractions[point])))},pm2rdm~{",".join(position)},pm2gnm '
    photo = site4 + params
    bot.send_photo(str(update.effective_chat['id']), photo=photo)


def find_attractions():
    global pos, position, site5
    ids = []
    ids_with_images = []
    response = requests.get(site5, params={
        'radius': '2000',
        'lon': position[0],
        'lat': position[1],
        'apikey': KEY
    })
    for i in response.json().keys():
        if i != 'type':
            for j in response.json()[i]:
                ids.append(j['id'])
    for i in ids:
        response2 = requests.get(site2 + i + '?', params={
            'apikey': KEY
        })
        if response2.json().get('image') is not None and response2.json().get('name') is not None:
            ids_with_images.append(i)
            pos = [response2.json().get('point')['lon'], response2.json().get('point')['lat']]
            response2 = requests.get(
                site2 + i + '?', params={
                    'apikey': KEY
                })
            atractions[response2.json()['name']] = pos
    return ids_with_images


def attractions(update: Update, context):
    global pos
    information = find_attractions()
    for i in information:
        response2 = requests.get(
            site2 + i + '?', params={
                'apikey': KEY
            })
        update.message.reply_text(
            text=response2.json()['name'], reply_markup=KEYBOARD)
        update.message.reply_photo(photo=response2.json()['image'])


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    buttons_handeler = CallbackQueryHandler(callback=button_handler_attractions)

    dp.add_handler(MessageHandler(Filters.contact | Filters.location, location))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('samara', attractions))
    dp.add_handler(CommandHandler('map', create_map))
    dp.add_handler(buttons_handeler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()