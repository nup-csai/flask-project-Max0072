# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN python -m venv venv \
    && . venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Экспонируем порт
EXPOSE 8080

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=server.py
ENV FLASK_ENV=production

# Запускаем Flask приложение
CMD ["/app/venv/bin/flask", "--app", "server.py", "run", "-h", "0.0.0.0", "-p", "8080"]

