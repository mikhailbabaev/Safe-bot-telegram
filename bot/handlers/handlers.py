import asyncio
import random
import os
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from keyboards import start_menu, FAQ, payments
from templates import SECURITY_STEPS ,get_random_result, progress_bar, WELCOME_MESSAGE, FAQ_TEXT, PAYMENT_TEXT


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):

    await message.answer(WELCOME_MESSAGE, reply_markup=start_menu)


async def animated_typing(callback, message):
    """Мигающий эффект '...' в процессе загрузки"""
    for _ in range(3):
        for dots in [".", "..", "...", ""]:
            await message.edit_text(f"⏳ Идёт проверка безопасности{dots}")
            await asyncio.sleep(0.5)


async def animated_typing(callback, message):
    """Мигающий эффект '...' перед началом проверки"""
    for _ in range(3):
        for dots in [".", "..", "...", ""]:
            await message.edit_text(f"⏳ Идёт проверка безопасности{dots}")
            await asyncio.sleep(0.5)


@router.callback_query(F.data == "check_security")
async def check_security(callback: CallbackQuery):
    """Имитация проверки безопасности с красивым прогрессом"""

    # # Отправляем стартовое сообщение
    # message = await callback.message.answer("⏳ Инициализация проверки...")
    # await callback.answer()
    #
    # # Мигающая анимация загрузки перед стартом
    # await animated_typing(callback, message)
    #
    # # Проходим по этапам проверки
    # for text, percent in SECURITY_STEPS:
    #     delay = random.uniform(1.5, 3)  # Рандомная задержка от 1.5 до 3 сек
    #     await asyncio.sleep(delay)
    #     await message.edit_text(f"{text}...\n{progress_bar(percent)}")
    # await asyncio.sleep(2)
    # await message.edit_text(f"{get_random_result()} 🔒")
    await callback.message.answer("🔧 Функция анализа уязвимостей в разработке. Запустим через месяц.")
    await callback.answer(show_alert=False)


@router.callback_query(F.data == "FAQ")
async def show_faq(callback: CallbackQuery):
    """Показываем информацию о FAQ с кнопкой возврата в главное меню"""

    # Обновляем сообщение с новым текстом и клавиатурой FAQ
    await callback.message.answer(
        FAQ_TEXT,  # Ссылка скрыта под текстом
        reply_markup=FAQ,  # Это клавиатура с кнопкой возврата в главное меню
        parse_mode="Markdown"  # Указываем, что используем Markdown
    )
    await callback.answer()


@router.callback_query(F.data == "go_to_start_menu")
async def return_to_main_menu(callback: CallbackQuery):
    """Возвращаем в главное меню с обновленным текстом"""

    # Обновляем текст и клавиатуру на главную
    await callback.message.answer(
        WELCOME_MESSAGE,
        reply_markup=start_menu  # Главная клавиатура
    )
    await callback.answer()  # Подтверждение нажатия


@router.callback_query(F.data == "payments")
async def payment_to_ukassa(callback: CallbackQuery):
    """Оплата сервиса через Юкассу"""

    # Закомментировали основной код
    # image_path = os.path.join(os.path.dirname(__file__), '../pay.jpg')
    # image_file = FSInputFile(image_path)
    # await callback.message.answer_photo(
    #     image_file,
    #     caption=PAYMENT_TEXT,
    #     reply_markup=payments,
    #     parse_mode='HTML'
    # )

    # Заглушка
    await callback.message.answer("💳 Функция оплаты в разработке. Запустим через месяц.")
    await callback.answer(show_alert=False)


@router.callback_query(F.data == "reference")
async def reference_info(callback: CallbackQuery):
    """Временно заглушка на функцию промокодов"""
    await callback.message.answer("🎟 Функция промокодов в разработке. Запустим через месяц.")
    await callback.answer(show_alert=False)