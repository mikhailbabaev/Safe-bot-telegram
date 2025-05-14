from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import REFERENCE, TO_MAIN_MENU, UKASSA_PAYMENT, PROMOCODE, UKASSA_PAY_URL


def get_payment_menu_kb(price: float, wallet: int)-> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=UKASSA_PAYMENT.format(price=price), callback_data='url_ukassa')],
            [InlineKeyboardButton(text=PROMOCODE, callback_data='use_promocode')],
            [InlineKeyboardButton(text=REFERENCE.format(wallet=wallet), callback_data="cashback")],
            [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
        ])


def get_payment_url_kb(payment_url: str, price: float) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=UKASSA_PAY_URL.format(price=price), url=payment_url)],
            [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data="go_to_start_menu")]
        ]
    )
