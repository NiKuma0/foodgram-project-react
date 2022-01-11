# Продуктовый помощник
## Описание
Веб приложения для публикации рецептов и составления списка покупок.

Мой дипломный проект! 
[Practicum](https://practicum.yandex.ru/) любезно предоставил готовую часть 
frontend-а
## Технологии
* frontend - написан с помощью фреймворка [React](https://reactjs.org/) на языке javascript

Backend был написан с помощью нескольких фреймворков для [python](https://python.org):
* [Django](https://www.djangoproject.com/) - основной фреймворк.
* [Django Rest framework](https://www.django-rest-framework.org/) - 
дополнение для django. Нужен для написания API
***
## Развёртывание проекта в docker контейнерах
1. Для начала нужно клонировать этот проект, и убедится что у вас есть 
docker

    ```Shell
    $ git clone https://github.com/NiKuma0/foodgram-project-react.git
    $ docker --version
    ```

2. В случае если docker'а у вас нет - установите его 
[здесь](https://www.docker.com/get-started).
3. Теперь, в корне проекта создайте файл `.env` - здесь будут основные настройки. 
4. Заполните его примерно так:
    ```shell
    DB_ENGINE=django.db.backends.postgresql 
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=''
    HOST='http://localhost/'
    ```
5. Запускаем!
    ```shell
    $ cd infra/ && docker-compose up
    ```