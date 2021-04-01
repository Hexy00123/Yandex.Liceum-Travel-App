import sys
import geocoder
import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from config import URL, site, get_attraction, get_map, find_all_attractions, KEY, PATH


class MainWindowApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # иницилизация переменых, получение позиции и подключение кнопок
        uic.loadUi(PATH + 'main_window_style.ui', self)
        self.get_position()
        self.init_constants()
        self.connect_buttons()

    def connect_buttons(self):
        # подключение кнопок
        self.find_attractions.clicked.connect(self.show_attractions)
        self.list_attractions.itemClicked.connect(self.selection_changed)

    def get_position(self):
        # получение местоположения
        self.position = geocoder.ip('me').latlng[::-1]

    def init_constants(self):
        # инициализирование переменных
        self.ids = []
        self.ids_with_images = []
        self.atractions = {}
        self.position = []

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
                                                             response2.json()['info']['descr']]

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
        self.window_description = DescriptionWindow(item.text(), self.atractions,
                                                    self.position)
        self.window_description.show()


class DescriptionWindow(QMainWindow):
    def __init__(self, name, attractions, position):
        super().__init__()
        uic.loadUi(PATH + 'style_window_information.ui', self)
        # инициализация переменных, получение фото карты, получение описания, вставка фото
        self.setWindowTitle(name)
        self.make_up()
        self.pixmap = QPixmap()
        self.name = name
        self.attractions = attractions
        self.position = position
        self.create_map(name)
        self.create_photo()
        self.create_description()

    def make_up(self):
        # небольшие косметические поправки
        self.label.move(10, 10)
        self.label.resize(430, 500)
        self.label.setScaledContents(False)
        self.adress.resize(500, 20)
        self.inform.move(10, 3)
        self.inform.setWordWrap(True)
        self.inform.resize(440, 650)
        self.inform.setStyleSheet('font-size:16px')

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

    def create_photo(self):
        # получение фотографии места
        r = requests.get(self.attractions[self.name][-1]).content
        self.pixmap.loadFromData(r)
        self.pixmap.scaled(430, 500)
        self.label.setPixmap(self.pixmap)
        self.image_map.move(10, 10)
        self.image_map.resize(430, 500)
        self.image_map.setScaledContents(False)

    def create_map(self, point):
        # создании карты с местоположением места
        pos = ",".join(list(map(str, self.position)))
        pos_attraction = ",".join(list(map(str, self.attractions[point][:2])))
        params = f'll={pos}&l=map&pt={pos_attraction},pm2rdm~{pos},pm2gnm'
        pixmap = QPixmap()
        pixmap.loadFromData(requests.get(get_map + params).content)
        pixmap.scaled(430, 500)
        self.image_map.setPixmap(pixmap)

    def favorites(self):
        # get запрос избранных пользователя
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
        if req.json().get('result')['message'] == 'OK':
            self.main = MainWindowApp()
            self.main.show()
            self.close()

    def registration(self):
        # вызов функции
        self.get_registr(self.login_line.text(), self.password_line.text())


# окно входа
class SignInWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(PATH + 'authentication_widget.ui', self)
        self.setWindowTitle("Вход")

    def connect_buttons(self):
        # подключение кнопок
        self.authentificate_button.clicked.connect(self.login)

    def authorization(self, mail, password):
        # получение результата запроса на вход
        req = requests.get(f'{URL}/api/auto/{mail}/{password}')
        if req.json().get('result')['message'] == 'OK':
            self.main = MainWindowApp()
            self.main.show()
            self.close()

    def login(self):
        # вызов функции
        self.authorization(self.login_line.text(), self.password_line.text())


# отладочная функция для показа ошибок, удалить на релизе
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # подключила главное окно для отладки, чтобы запустить полность замени класс на StartWindow
    ex = MainWindowApp()
    ex.show()
    # отладочная функция для показа ошибок, удалить на релизе
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    sys.excepthook = except_hook
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    sys.exit(app.exec_())
