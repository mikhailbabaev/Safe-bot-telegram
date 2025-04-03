import random
import string
import hashlib

from sqlalchemy import ForeignKey


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
    table_name = camel_case_to_snake(reference.__name__)  # Преобразуем имя класса в snake_case
    return ForeignKey(f"{table_name}s.{column}")  # Добавляем 's' для таблицы и указываем столбец