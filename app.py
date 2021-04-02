from flask import request, jsonify, Flask, Blueprint, make_response
from model import *
from config import post_login, post_password
import smtplib

app = Flask(__name__)


@app.route('/api/reg/<mail>/<password>', methods=['POST'])
def register(mail, password):
    if not bool(User.select().where(User.email == mail)):
        try:
            user_id = max(i.id for i in User.select()) + 1
        except ValueError:
            user_id = 1
        User.create(id=user_id, email=mail, password=password, favorites='', anket_id=0)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(post_login, post_password)

        text = 'Данная почта была зарегестрирована в приложении'

        text = "\r\n".join([
            "Subject: Регистрация нового пользователя",
            str(text)
        ])

        server.sendmail(post_login, mail, text.encode('utf-8'))
        server.quit()

        return make_response(jsonify({'result': {'message': 'OK', 'id': user_id}}), 200)

    else:
        return make_response(jsonify({'result': {'message': 'Данная почта уже зарегестрирована'}}),
                             404)


@app.route('/api/auto/<mail>/<password>', methods=['GET'])
def authorisation(mail, password):
    try:
        user = User.get(User.email == mail)
        if password != user.password:
            return make_response(jsonify({'result': {'message': 'Неверный пароль'}}), 404)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(post_login, post_password)

        text = 'В ваш аккаунт был выполнен вход'

        text = "\r\n".join([
            "Subject: Авторизация пользователя",
            str(text)
        ])

        server.sendmail(post_login, mail, text.encode('utf-8'))
        server.quit()

        return make_response(jsonify({'result': {'message': 'OK', 'id': user.id}}), 200)
    except:
        return make_response(jsonify({'result': {'message': 'Данная почта не зарегестрирована'}}),
                             404)


@app.route('/api/favorites/<user_id>/<place_id>', methods=['POST'])
def add_favorites(user_id, place_id):
    if bool(User.select().where(User.id == user_id)):
        user = User.get_by_id(user_id)
        if user.anket_id == 0:
            return make_response(jsonify({'result': {'message': 'Добавлять в избранное могут '
                                                                'только пользователи с '
                                                                'заполенной анкетой'}}), 404)
        if place_id + ';' not in user.favorites:
            user.favorites += f'{place_id};'
            user.save()
            return make_response(jsonify({'result': {'message': 'OK'}}), 200)
        else:
            return make_response(jsonify({'result': {'message': 'Данное место уже есть в списке'}}),
                                 404)


    else:
        return make_response(jsonify({'result': {'message': 'Такого id не существует'}}), 404)


@app.route('/api/favorites/<user_id>', methods=['GET'])
def send_favorites(user_id):
    if bool(User.select().where(User.id == user_id)):
        user = User.get_by_id(user_id)
        answer = [favorite for favorite in user.favorites.split(';')[:-1]]
        return make_response(jsonify({'result': {'message': 'OK',
                                                 'favorites': answer}}), 200)
    else:
        return make_response(jsonify({'result': {'message': 'Такого id не существует'}}), 404)


@app.route('/api/anket/<user_id>', methods=['POST'])
def anket(user_id):
    args = request.args
    surname = args.get('surname')
    name = args.get('name')
    secondname = args.get('secondname')

    try:
        anket_id = max(i.id for i in Anket.select()) + 1
    except ValueError:
        anket_id = 1
    Anket.create(id=anket_id, surname=surname, name=name, secondname=secondname)
    user = User.get_by_id(user_id)
    user.anket_id = anket_id
    user.save()

    return make_response(jsonify({'result': {'message': 'OK'}}), 200)


@app.route('/api/anket/<anket_id>', methods=['GET'])
def get_anket(anket_id):
    anket = Anket.get_by_id(anket_id)
    return make_response(jsonify({'result': {'message': 'OK',
                                             'surname': anket.surname,
                                             'name': anket.name,
                                             'secondname': anket.secondname}}), 200)


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.get_by_id(user_id)
    favorites = [favorite for favorite in user.favorites.split(';')[:-1]]
    return make_response(jsonify({'result': {'message': 'OK',
                                             'email': user.email,
                                             'favorites': favorites,
                                             'anket_id': user.anket_id}}), 200)


@app.route('/api/APP_IS_WORKING', methods=['GET'])
def app_is_working():
    return 'app_is_working'


@app.route('/', methods=['GET'])
def start_page():
    return 'Это просто API, тут не должно быть стартовой страницы, на которой вы и находитесь'


if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1', debug=True)
