import asyncio
import logging
import random
import string
import hashlib

from sqlalchemy import ForeignKey
from aiogram import Dispatcher

logger = logging.getLogger(__name__)


def generate_promocode(tg_id: int) -> str:
    """Генерируем уникальный промокод на основе tg_id"""
    hash_part = hashlib.md5(str(tg_id).encode()).hexdigest()[:4]
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"SAFE-{hash_part}-{random_part}"


def camel_case_to_snake(input_str: str) -> str:
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append('_')
        chars.append(char.lower())
    return ''.join(chars)


def fk(reference: type, column: str = "id") -> ForeignKey:
    """Генерирует ForeignKey, используя `camel_case_to_snake` для имени таблицы и поля."""
    table_name = camel_case_to_snake(reference.__name__)
    return ForeignKey(f"{table_name}s.{column}")


def get_user_achievement_text(achievement_number: int, achievement_list: list) -> str:
    """Генерирует текст с достижениями по номеру."""
    received = []
    not_received = []

    for i in range(1, len(achievement_list) + 1):
        achievement_text = achievement_list[i].split(" (")[0]  # Оставляем только текст до (число/10)
        if i <= achievement_number:
            received.append(achievement_text)
        else:
            not_received.append(achievement_text)

    return f"Ваши достижения {achievement_number} из 10\n\n" \
           f"Получены:\n" + "\n".join(received) + "\n\n" \
           f"Не получены:\n" + "\n".join(not_received)


async def on_shutdown(dispatcher: Dispatcher, poll_task: asyncio.Task):
    logging.info("🛑 Завершение работы бота...")

    # Завершаем фоновую задачу
    if not poll_task.done():
        logging.info("❌ Завершаем фоновую задачу poll_unpaid_payments.")
        poll_task.cancel()

    try:
        await poll_task
    except asyncio.CancelledError:
        logging.info("Задача poll_unpaid_payments завершена.")


    # Закрываем соединение с БД
    logging.info("Закрытие соединения с БД...")
    await dispatcher.workflow_data["db_helper"].dispose()
    logging.info("✅ Соединение с БД закрыто.")