from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import REFERENCE, TO_MAIN_MENU, UKASSA_PAYMENT, PROMOCODE



def create_payments_keyboard(payment_url: str) -> InlineKeyboardMarkup:
    """Создание клавиатуры с кнопкой для оплаты через Юкассу"""
    payments = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=UKASSA_PAYMENT, url=payment_url)],
        [InlineKeyboardButton(text=PROMOCODE, callback_data='use_promocode')],
        [InlineKeyboardButton(text=REFERENCE, callback_data='cashback')],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])
    return payments