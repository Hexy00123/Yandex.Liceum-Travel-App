from flask import request, jsonify, Flask, Blueprint, make_response
from model import *
from config import post_login, post_password
import smtplib
import os
import rebuild_database


app = Flask(__name__)


@app.route('/api/reg/<mail>/<password>', methods=['POST'])
def register(mail, password):
    if not bool(User.select().where(User.email == mail)):
        try:
            user_id = max(i.id for i in User.select()) + 1
        except ValueError:
            user_id = 1
        User.create(id=user_id, email=mail, password=password, anket_id=0)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(post_login, post_password)

        text = f'Ваша почта: {mail} была зарегестрирована в приложении для определения ближайших' \
               f'достопримечательностей'

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
        if not bool(UserPlaces.select().where(
                (UserPlaces.user_id == user_id) & (UserPlaces.place_id == place_id))):
            try:
                id = max(i.id for i in UserPlaces.select()) + 1
            except ValueError:
                id = 1

            UserPlaces.create(user_id=user_id, place_id=place_id, comment='', id=id)

            if bool(Place.select().where(Place.id == place_id)):
                place = Place.select().where(Place.id == place_id)[0]
                place.added_to_favorites += 1
                place.save()
            else:
                Place.create(id=place_id, added_to_favorites=1)

            return make_response(jsonify({'result': {'message': 'OK'}}), 200)
        else:
            return make_response(jsonify({'result': {'message': 'Данное место уже есть в списке'}}),
                                 404)


    else:
        return make_response(jsonify({'result': {'message': 'Такого id не существует'}}), 404)


@app.route('/api/favorites/<user_id>', methods=['GET'])
def send_favorites(user_id):
    if bool(User.select().where(User.id == user_id)):
        places = UserPlaces.select().where(UserPlaces.user_id == user_id)
        answer = []

        for place in places:
            answer.append(place.place_id)

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
    return make_response(jsonify({'result': {'message': 'OK',
                                             'email': user.email,
                                             'anket_id': user.anket_id}}), 200)


@app.route('/api/place/<place_id>', methods=['GET'])
def get_place(place_id):
    place_id = int(place_id)
    place = Place.get_or_none(id=place_id)
    if place is not None:
        comments = []
        for record in UserPlaces.select().where(UserPlaces.place_id == place_id):
            comments.append([record.user_id, record.comment])

        return make_response(jsonify({'result': {'message': 'OK',
                                                 'added_to_favorites': place.added_to_favorites,
                                                 'comments': comments}}),
                             200)
    else:
        return make_response(jsonify({'result': {'message': 'OK',
                                                 'added_to_favorites': 0}}), 200)


@app.route('/api/comments', methods=['POST'])
def add_comment():
    args = request.args
    user_id = int(args.get('user_id'))
    place_id = int(args.get('place_id'))
    comment = args.get('comment')

    if bool(UserPlaces.select().where(
            (UserPlaces.user_id == user_id) & (UserPlaces.place_id == place_id))):
        post = \
            UserPlaces.select().where((
                                              UserPlaces.user_id == user_id) & (
                                              UserPlaces.place_id == place_id))[0]
        post.comment = comment
        post.save()
        return make_response(jsonify({'result': {'message': 'OK'}}), 200)
    else:
        return make_response(jsonify({'result': {'message': 'Такой записи не существует'}}), 404)


@app.route('/api/comments/<user_id>/<place_id>', methods=['GET'])
def get_comment(user_id, place_id):
    user_id, place_id = int(user_id), int(place_id)
    print([i.place_id for i in UserPlaces.select().where(
        (UserPlaces.place_id == place_id) & (UserPlaces.user_id == user_id))])

    if bool(UserPlaces.select().where(
            (UserPlaces.place_id == place_id) & (UserPlaces.user_id == user_id))):
        post = \
            UserPlaces.select().where(
                (UserPlaces.place_id == place_id) & (UserPlaces.user_id == user_id))[0]

        return make_response(jsonify({'result': {'message': 'OK',
                                                 'comment': post.comment}}), 200)
    else:
        return make_response(jsonify({'result': {'message': 'Такой записи не существует'}}), 404)


@app.route('/api/APP_IS_WORKING', methods=['GET'])
def app_is_working():
    return 'app_is_working'


@app.route('/', methods=['GET'])
def start_page():
    return 'Это просто API, тут не должно быть стартовой страницы, на которой вы и находитесь'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
