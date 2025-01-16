# 1. Используем официальный образ Python как базовый
FROM python:3.12-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# 4. Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем все файлы проекта в контейнер
COPY . .

# 6. Открываем нужный порт для Flask
EXPOSE 5000

# 7. Устанавливаем переменную окружения для Flask (если требуется)
ENV FLASK_APP=server.py

# 8. Устанавливаем команду для запуска приложения (для Flask)
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

## Для Django
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

