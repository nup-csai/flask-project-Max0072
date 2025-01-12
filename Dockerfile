# Шаг 1: Используем официальный образ Python
FROM python:3.9-slim

# Шаг 2: Установим зависимости системы для работы с SQLite и другими библиотеками
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Шаг 3: Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Шаг 4: Копируем файлы requirements.txt и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Шаг 5: Копируем весь проект в контейнер
COPY . /app/

# Шаг 6: Экспонируем порт 5000, который будет использовать Flask
EXPOSE 5000

# Шаг 7: Устанавливаем переменные окружения для Flask
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Шаг 8: Запускаем приложение с помощью Gunicorn (для продакшн-среды)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
