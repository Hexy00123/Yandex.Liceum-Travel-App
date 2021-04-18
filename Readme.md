    Наше приложение создано для туристов, которые приехали в тот или иной город и хотят посмотреть и запомнить его особые места.
Для этого в нашем приложении реализована функция создания аккаунтов и входа в них для каждого пользователя, после регистрации/входа 
конкретному пользователю на его электронну почту приходит письмо-уведомление.

В самом приложении реализованны функции: поиск ближайших достопримечательнностей по вашему местоположению с помощью стороннего api, добавление мест в избранное 
пользователя, а также есть профиль пользователя, которой нужно заполнить, если вы хотите пользоваться всеми функциями приложения.

Все данные от пользователя отправляются на сервер, в котором мы построили собственное api, с помощью фреймворка flask и сохраняются в 
базе данных, которая управляется с помощью библиотеки peewee. Как сервер, так и база данных загружены на Heroku.

Структура приложения разделена на 2 части: сервер и клиент - все эти части приложения работают совместно

Сервер реализован с помощью фреймворка flask и с помощью функции запросов предоставляет клиенту функцию работы с базой данных, структуру которой вы можете проследить на изображении ниже.

Клиент реализован с помощью фреймворка PyQt5, и графический интерфейс для пользователя и пользуется аппаратным интерфейсом сервера.


![database_diagram](https://github.com/Hexy00123/YLProject/blob/Resourses/database_sheme.jpg)


