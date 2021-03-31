from flask import request, jsonify, Flask, Blueprint, make_response
from model import *

app = Flask(__name__)
db = []


@app.route('/api/reg/<mail>/<password>', methods=['POST'])
def register(mail, password):
    if not bool(User.select().where(User.email == mail)):
        try:
            user_id = max(i.id for i in User.select()) + 1
        except ValueError:
            user_id = 1
        User.create(id=user_id, email=mail, password=password)
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
        return make_response(jsonify({'result': {'message': 'OK', 'id': user.id}}), 200)
    except:
        return make_response(jsonify({'result': {'message': 'Данная почта не зарегестрирована'}}),
                             404)


if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1', debug=True)