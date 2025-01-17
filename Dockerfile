# 1. Используем официальный образ Python как базовый
FROM python:3.9-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# 4. Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем Gunicorn
RUN pip install gunicorn

# 5. Копируем все файлы проекта в контейнер
COPY . .

# 6. Открываем порт для Flask-приложения (например, 5000 или 8000)
EXPOSE 8000

# 7. Устанавливаем переменную окружения для Flask
ENV FLASK_APP=server.py


# 8. Устанавливаем команду для запуска приложения Flask
CMD ["python", "server.py"]

#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server:app"]


