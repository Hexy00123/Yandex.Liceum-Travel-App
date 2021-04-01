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
        User.create(id=user_id, email=mail, password=password, favorites='')

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

        return make_response(jsonify({'result': {'message': 'OK'}}), 200)

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
        user.favorites += f';{place_id}'
        user.save()
        return make_response(jsonify({'result': {'message': 'OK'}}), 200)
    else:
        return make_response(jsonify({'result': {'message': 'Такого id не существует'}}), 404)


@app.route('/api/favorites/<user_id>', methods=['GET'])
def send_favorites(user_id):
    if bool(User.select().where(User.id == user_id)):
        user = User.get_by_id(user_id)
        answer = [favorite for favorite in user.favorites.split(';')]
        return make_response(jsonify({'result': {'message': 'OK',
                                                 'favorites': answer}}), 200)
    else:
        return make_response(jsonify({'result': {'message': 'Такого id не существует'}}), 404)


if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1', debug=True)
