from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import REFERENCE, TO_MAIN_MENU, UKASSA_PAYMENT, PROMOCODE


def get_payment_menu_kb(price: float)-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=UKASSA_PAYMENT.format(price=price), callback_data='url_ukassa')],
            [InlineKeyboardButton(text=PROMOCODE, callback_data='use_promocode')],
            [InlineKeyboardButton(text=REFERENCE, callback_data='cashback')],
            [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
        ])


payments = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=UKASSA_PAYMENT, callback_data='url_ukassa')],
        [InlineKeyboardButton(text=PROMOCODE, callback_data='use_promocode')],
        [InlineKeyboardButton(text=REFERENCE, callback_data='cashback')],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def get_payment_url_kb(payment_url: str, price: float) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=UKASSA_PAYMENT.format(price=price), url=payment_url)],
            [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data="go_to_start_menu")]
        ]
    )
