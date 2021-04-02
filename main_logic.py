import sys
import geocoder
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from config_client import URL, site, get_attraction, get_map, find_all_attractions, KEY, PATH


class MainWindowApp(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        # иницилизация переменых, получение позиции и подключение кнопок
        uic.loadUi(PATH + 'main_window_style.ui', self)
        self.user_id = user_id
        self.init_constants()
        self.get_position()
        self.connect_buttons()
        # удалить на релизе
        #requests.get(f'{URL}/api/APP_IS_WORKING')
        # . . . . . . . . . . . . . . . . . .
        self.show_favorites(self.favorites_id)

    def init_constants(self):
        # инициализирование переменных34
        self.ids = []
        self.ids_with_images = []
        self.atractions = {}
        self.position = []
        self.favorites_id = self.get_favorites()
        print(self.favorites_id)
        self.favorites = {}

    def connect_buttons(self):
        # подключение кнопок
        self.find_attractions.clicked.connect(self.show_attractions)
        self.list_attractions.itemClicked.connect(self.selection_changed)
        self.listWidget.itemClicked.connect(self.selection_favorite)

    def get_position(self):
        # получение местоположения
        self.position = geocoder.ip('me').latlng[::-1]

    def search_attractions(self):
        # поиск мест
        self.ids.clear()
        self.ids_with_images.clear()
        self.get_position()

        # получение достопримечательностей
        response = requests.get(find_all_attractions, params={
            'radius': '1500',
            'lon': self.position[0],
            'lat': self.position[1],
            'apikey': KEY
        })

        # сортировка достопримечательностей по наличию фото и названия
        for i in response.json().keys():
            if i != 'type':
                for j in response.json()[i]:
                    self.ids.append(j['id'])
        for i in self.ids:
            response2 = requests.get(get_attraction + i + '?', params={
                'apikey': KEY
            })
            if response2.json().get('image') is not None and response2.json().get(
                    'name') is not None and 'wikimedia' not in response2.json().get('image'):
                self.ids_with_images.append(i)
                self.atractions[response2.json()['name']] = [response2.json().get('point')['lon'],
                                                             response2.json().get('point')['lat'],
                                                             response2.json()['info']['descr'],
                                                             i]
        # возвращение id отсортированных достопримечательностей
        return self.ids_with_images

    def show_attractions(self):
        # показ списка достопримечательностей
        self.list_attractions.clear()
        for i in self.search_attractions():
            response2 = requests.get(
                get_attraction + i + '?', params={
                    'apikey': KEY
                }).json()
            try:
                self.list_attractions.addItem(response2['name'])
                self.atractions[response2['name']].append(response2['image'])
            except KeyError:
                pass

    def selection_changed(self, item):
        # открытие второго окна с описанием
        self.get_position()
        self.window_description = DescriptionWindow(item.text(), self.atractions,
                                                    self.position, [self.user_id, self.atractions[item.text()][3]])
        self.window_description.show()
        self.update_favorites()

    def get_favorites(self):
        # get запрос избранных пользователя присваевается резульата self.favorites_id
        req = requests.get(f'{URL}/api/favorites/{self.user_id}')
        print(req.status_code)
        if req.status_code == 200:
            return req.json()['result']['favorites']
        return None

    def show_favorites(self, source):
        # показ избранных в списке
        #source.remove('')
        if len(source) != 0:
            for i in source:
                response = requests.get(
                    get_attraction + i + '?',
                    params={
                        'apikey': KEY
                    })
                self.favorites[response.json()['name']] = [response.json().get('point')['lon'],
                                                           response.json().get('point')['lat'],
                                                           response.json()['info']['descr'],
                                                           i,
                                                           response.json()['image']]
                self.listWidget.addItem(response.json()['name'])

    def selection_favorite(self, item):
        # открытие окна избранного
        self.window_favorite = DescriptionWindow(item.text(), self.favorites,
                                                    self.position, [self.user_id, self.favorites[item.text()][3]])
        self.window_favorite.show()
        self.update_favorites()

    def update_favorites(self):
        # обновление избранных во время работы приложений
        self.listWidget.clear()
        self.favorites_id = self.get_favorites()
        self.show_favorites(self.favorites_id)


class DescriptionWindow(QMainWindow):
    def __init__(self, name, attractions, position, user_id_attraction):
        super().__init__()
        uic.loadUi(PATH + 'style_window_information.ui', self)
        # инициализация переменных, получение фото карты, получение описания, вставка фото
        self.setWindowTitle(name)
        self.make_up()
        self.pixmap = QPixmap()
        self.user_id_attraction = user_id_attraction
        self.name = name
        self.attractions = attractions
        self.position = position
        self.connect_butttons()
        self.create_map(name)
        self.set_photo()
        self.create_description()

    def connect_butttons(self):
        self.pushButton.clicked.connect(self.add_favorites)

    def make_up(self):
        # небольшие косметические поправки
        self.label.setScaledContents(False)
        self.inform.setWordWrap(True)

    def create_description(self):
        # получение описания места
        req = requests.get(site, params={
            'geocode': ', '.join(list(map(str, self.attractions[self.name][:2]))),
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'format': 'json',
            'kind': 'house'
        })
        text = self.attractions[self.name][2].replace('<p>', '').replace('</p>', '')
        self.adress.setText(
            req.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']['text'])
        self.inform.setText(text)

    def set_photo(self):
        # получение фотографии места
        r = self.create_photo(self.attractions)
        self.pixmap.loadFromData(r)
        self.pixmap.scaled(430, 500)
        self.label.setPixmap(self.pixmap)
        self.image_map.move(10, 10)
        self.image_map.resize(430, 500)
        self.image_map.setScaledContents(False)

    def create_photo(self, source):
        return requests.get(source[self.name][-1]).content

    def create_map(self, point):
        # создании карты с местоположением места
        pos = ",".join(list(map(str, self.position)))
        pos_attraction = ",".join(list(map(str, self.attractions[point][:2])))
        params = f'll={pos}&l=map&pt={pos_attraction},pm2rdm~{pos},pm2gnm'
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(get_map + params).content)
        pixmap.scaled(430, 500)
        self.image_map.setPixmap(pixmap)

    def add_favorites(self):
        # запрос на добавление избранных пользователя
        r = requests.post(f'{URL}/api/favorites/{self.user_id_attraction[0]}/{self.user_id_attraction[1]}')
        if r.status_code == 404:
            QMessageBox.critical(self, 'Error 404', r.json()['result']['message'])
        print(r.status_code)
        pass


# стартовое окно
class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(PATH + 'start_widget.ui', self)
        self.setWindowTitle('Приветствую вас')
        self.connect_buttons()

    def connect_buttons(self):
        # подключение кнопок
        self.sing_up_dec_button.clicked.connect(self.registration)
        self.sing_in_dec_button.clicked.connect(self.sign_in)

    def registration(self):
        # открытие окно регмстрации
        self.sign_up_window = RegistartionWindow()
        self.sign_up_window.show()
        self.close()

    def sign_in(self):
        # открытие окно входа
        self.sign_in_window = SignInWindow()
        self.sign_in_window.show()
        self.close()


# окно регистрации
class RegistartionWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(PATH + 'registration_widget.ui', self)
        self.setWindowTitle("Регистрация")
        self.connect_buttons()

    def connect_buttons(self):
        # подключение кнопок
        self.authentificate_button.clicked.connect(self.registration)

    def get_registr(self, mail, password):
        # получение результата запроса на регистрацию
        req = requests.post(f'{URL}/api/reg/{mail}/{password}')
        print(req.json())
        if req.status_code == 200:
            self.main = MainWindowApp(req.json()['result']['id'])
            self.main.show()
            self.close()
        elif req.status_code == 404:
            QMessageBox.critical(self, 'Error 404', req.json()['result']['message'])

    def registration(self):
        # вызов функции
        self.get_registr(self.login_line.text(), self.password_line.text())


# окно входа
class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(PATH + 'authentication_widget.ui', self)
        self.setWindowTitle("Вход")
        self.connect_buttons()

    def connect_buttons(self):
        # подключение кнопок
        self.authentificate_button.clicked.connect(self.login)

    def authorization(self, mail, password):
        # получение результата запроса на вход
        req = requests.get(f'{URL}/api/auto/{mail}/{password}')
        if req.status_code == 200:
            self.main = MainWindowApp(req.json()['result']['id'])
            self.main.show()
            self.close()
        elif req.status_code == 404:
            QMessageBox.critical(self, 'Error 404', req.json()['result']['message'])

    def login(self):
        # вызов функции
        self.authorization(self.login_line.text(), self.password_line.text())


# отладочная функция для показа ошибок, удалить на релизе
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # подключила главное окно для отладки, чтобы запустить полность замени класс на StartWindow
    ex = StartWindow()
    ex.show()
    # отладочная функция для показа ошибок, удалить на релизе
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    sys.excepthook = except_hook
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    sys.exit(app.exec_())
