#!/bin/bash

# Выводим сообщение и ждем, пока база станет доступной
echo "⌛ Waiting for database to be ready..."
until pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done

# Загружаем переменные окружения из .env
echo "📦 Loading environment variables..."
export $(grep -v '^#' .env | xargs)

# Выполняем миграции Alembic
echo "✅ Database is ready. Applying migrations..."
alembic upgrade head

# Запускаем бота
echo "🚀 Starting the bot..."
exec python bot/main.py
