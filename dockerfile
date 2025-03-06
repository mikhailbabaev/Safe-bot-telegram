# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (если нужно)
RUN apt-get update && apt-get install -y libpq-dev

# Дополнительно устанавливаем PostgreSQL клиент для использования pg_isready
RUN apt-get update && apt-get install -y postgresql-client

# Копируем только файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Создание виртуального окружения и активация его (если нужно)
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Команда для запуска бота
CMD ["python", "bot/bot.py"]
