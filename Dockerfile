# используем образ python 3.10
FROM python:3.10

# установка зависимостей
RUN pip install pipenv

# создание директории приложения в контейнере
RUN mkdir /app

# установка рабочей директории в /app
WORKDIR /app

# копирование Pipfile и Pipfile.lock в директорию /app
COPY requirements.txt /app/

# установка зависимостей из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# копирование кода приложения в контейнер
COPY . /app/
COPY ./staticfiles /app/static
RUN python manage.py collectstatic --noinput

# открытие порта 8000 для обращения к Django приложению через TCP/IP
EXPOSE 8000

# запуск приложения с помощью gunicorn
CMD gunicorn core.wsgi:application --bind 0.0.0.0:8000
