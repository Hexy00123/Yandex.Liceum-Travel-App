import sys
import geocoder
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from style import Ui_MainWindow
from style_window2 import Ui_MainWindow2

site2 = 'http://api.opentripmap.com/0.1/ru/places/xid/'
site3 = 'https://geocode-maps.yandex.ru/1.x/?'
site4 = 'https://static-maps.yandex.ru/1.x/?'
site5 = 'http://api.opentripmap.com/0.1/ru/places/radius?'
KEY = '5ae2e3f221c38a28845f05b611939fdf10b5f750f31efaf84a6fa7c0'


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.find_attractions.clicked.connect(self.run)
        self.list_attractions.itemClicked.connect(self.selectionChanged)
        self.atractions = {}
        self.position = []
        self.pos = []

    def search_attractions(self):
        ids = []
        ids_with_images = []
        response = requests.get(site5, params={
            'radius': '1500',
            'lon': self.position[1],
            'lat': self.position[0],
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
                self.atractions[response2.json()['name']] = pos

        return ids_with_images

    def run(self):
        pos = geocoder.ip('me')
        self.position = pos.latlng
        self.list_attractions.clear()
        information = self.search_attractions()
        for i in information:
            response2 = requests.get(
                site2 + i + '?', params={
                    'apikey': KEY
                }).json()
            try:
                self.list_attractions.addItem(response2['name'])
            except KeyError:
                pass
            # update.message.reply_text(
            #     text=response2.json()['name'], reply_markup=KEYBOARD)
            # update.message.reply_photo(photo=response2.json()['image'])
        # con = sqlite3.connect("Книги.sqlite")
        # cur = con.cursor()
        # self.name = self.lineEdit.text()
        # if self.comboBox.currentText() == 'Автор':
        #     result = cur.execute(f"""SELECT название FROM Books
        #     WHERE автор LIKE '%{self.name}%'""").fetchall()
        #     for i in result:
        # elif self.comboBox.currentText() == 'Название':
        #     result = cur.execute(f"""SELECT название FROM Books
        #                 WHERE название LIKE '%{self.name.lower()}%' """).fetchall()
        #     for i in result:
        #         self.tableWidget.addItem(*i)

    def selectionChanged(self, item):
        self.w2 = Window2(item.text())
        self.w2.show()


class Window2(QWidget, Ui_MainWindow2):
    def __init__(self, name):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(name)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
