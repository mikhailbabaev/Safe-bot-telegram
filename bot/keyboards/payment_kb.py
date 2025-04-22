from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import REFERENCE, TO_MAIN_MENU, UKASSA_PAYMENT, PROMOCODE

payments = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=UKASSA_PAYMENT, callback_data='url_ukassa')],
        [InlineKeyboardButton(text=PROMOCODE, callback_data='use_promocode')],
        [InlineKeyboardButton(text=REFERENCE, callback_data='cashback')],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def get_payment_url_kb(payment_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=UKASSA_PAYMENT, url=payment_url)],
            [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data="go_to_start_menu")]
        ]
    )
