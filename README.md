# My Awesome Django REST Framework Project

Этот проект представляет собой сервис для управления закладками.

## Установка и запуск через Docker

1. Клонируйте репозиторий:
    ```bash
   git clone https://github.com/your-username/your-project.git


2. Перейдите в директорию проекта:

    cd your-project

3. Проверьте наличие Docker:
    
    
    Перед тем как продолжить, убедитесь, что у вас установлен Docker. Вы можете проверить это командой:


    docker --version

    Если Docker не установлен, установите Docker согласно инструкциям для вашей операционной системы.


4. После запускаем проект
    находим где у нас docker-compose.yml
    
    sudo docker-compose build
    sudo docker-compose up


Теперь ваш сервер должен быть доступен по адресу http://0.0.0.0:8000/.
Использование API

    Документация API: http://127.0.0.1:8000/swagger/
    Админ-панель: http://127.0.0.1:8000/admin/


## Установка и запуск


1. Перейдите в директорию проекта:

    cd your-project

2. Создайте и активируйте виртуальное окружение:

    bash

    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate

3. Установите зависимости:

    bash

    pip install -r requirements.txt


4. Создать файл .env в каталоге drf_project где находиться settings.py файл

    и поставить вот это

    SECRET_KEY=foo
    DEBUG=1
    USE_SQLITE=1
    ALLOWED_HOSTS=0.0.0.0 localhost 127.0.0.1
    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

4. Примените миграции:

    bash
    
    python manage.py makemigrations
    python manage.py migrate

5. Запустите сервер:

    bash

    python manage.py runserver

    ```

Теперь ваш сервер должен быть доступен по адресу http://127.0.0.1:8000/api/.
Использование API

    Документация API: http://127.0.0.1:8000/swagger/
    Админ-панель: http://127.0.0.1:8000/admin/



На реализацию задачи ушло 13 часов