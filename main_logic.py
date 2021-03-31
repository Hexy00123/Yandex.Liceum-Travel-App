import sys
import geocoder
import requests
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap

from authentication_widget import Ui_Sign_in
from style_2 import Ui_MainWindow
from style_window_information import Ui_Window_Information
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from start_widget import Ui_Form
from registration_widget import Ui_Registration

site = 'https://geocode-maps.yandex.ru/1.x/?'
site2 = 'http://api.opentripmap.com/0.1/ru/places/xid/'
site3 = 'https://geocode-maps.yandex.ru/1.x/?'
site4 = 'https://static-maps.yandex.ru/1.x/?'
site5 = 'http://api.opentripmap.com/0.1/ru/places/radius?'
KEY = '5ae2e3f221c38a28845f05b611939fdf10b5f750f31efaf84a6fa7c0'

atractions = {}
position = []
list_information = {}


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        global list_information
        super().__init__()
        self.setupUi(self)
        self.find_attractions.clicked.connect(self.run)
        self.list_attractions.itemClicked.connect(self.selectionChanged)
        self.atractions_photo = {}
        self.position = []
        pos = geocoder.ip('me')
        self.position = pos.latlng
        self.position = self.position[::-1]
        self.pos = []
        self.URL = 'http://0f207db3e953.ngrok.io/'

    def search_attractions(self):
        ids = []
        ids_with_images = []
        response = requests.get(site5, params={
            'radius': '1500',
            'lon': self.position[0],
            'lat': self.position[1],
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
            if response2.json().get('image') is not None and response2.json().get(
                    'name') is not None and 'wikimedia' not in response2.json().get('image'):
                ids_with_images.append(i)
                pos = [response2.json().get('point')['lon'], response2.json().get('point')['lat']]
                atractions[response2.json()['name']] = pos
                list_information[response2.json()['name']] = response2.json()['info']['descr']
        return ids_with_images

    def run(self):
        pos = geocoder.ip('me')
        self.position = pos.latlng
        self.position = self.position[::-1]
        self.list_attractions.clear()
        information = self.search_attractions()
        for i in information:
            response2 = requests.get(
                site2 + i + '?', params={
                    'apikey': KEY
                }).json()
            try:
                self.list_attractions.addItem(response2['name'])
                self.atractions_photo[response2['name']] = response2['image']
            except KeyError:
                pass

    def selectionChanged(self, item):
        self.w2 = Window2(item.text(), self.atractions_photo[item.text()])
        self.w2.show()

    def registration(self, mail, password):
        requests.post(f'{self.URL}/api/reg/{mail}/{password}')

    def authorization(self, mail, password):
        print(requests.get(f'{self.URL}/api/auto/{mail}/{password}').json())


class Window2(QWidget, Ui_Window_Information):
    def __init__(self, name, photo):
        global list_information
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(name)
        r = requests.get(photo).content
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(r)
        self.label.move(10, 10)
        self.label.resize(430, 500)
        self.label.setScaledContents(False)
        self.pixmap.scaled(430, 500)
        self.label.setPixmap(self.pixmap)
        self.create_map(name)
        pos = geocoder.ip('me')
        self.position = pos.latlng
        p = ', '.join(list(map(str, atractions[name])))
        req = requests.get(site, params={
            'geocode': p,
            'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
            'format': 'json',
            'kind': 'house'
        })
        self.adress.resize(500, 20)
        text = list_information[name].replace('<p>', '')
        self.adress.setText(
            req.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
                'GeocoderMetaData']['text'])
        self.inform.setText(text)

    def create_map(self, point):
        pos = geocoder.ip('me')
        position = pos.latlng[::-1]
        position = list(map(str, position))
        params = f'll={",".join(position)}&l=map&pt={",".join(list(map(str, atractions[point])))},pm2rdm~{",".join(position)},pm2gnm'
        photo = site4 + params
        r = requests.get(photo).content
        pixmap = QPixmap()
        pixmap.loadFromData(r)
        self.image_map.move(10, 10)
        self.image_map.resize(430, 500)
        self.image_map.setScaledContents(False)
        pixmap.scaled(430, 500)
        self.image_map.setPixmap(pixmap)

    def favorites(self):
        pass


class StartWindow(QWidget, Ui_Form):
    def __init__(self):
        global list_information
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Приветствую вас')
        self.sing_up_dec_button.clicked.connect(self.registration)
        self.sing_in_dec_button.clicked.connect(self.sign_in)

    def registration(self):
        self.w = RegistartionWindow()
        self.w.show()
        self.close()

    def sign_in(self):
        self.w2 = SignInWindow()
        self.w2.show()
        self.close()


class RegistartionWindow(QWidget, Ui_Registration):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Регистрация")

    def registration(self):
        pass


class SignInWindow(QWidget, Ui_Sign_in):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Вход")

    def login(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StartWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
