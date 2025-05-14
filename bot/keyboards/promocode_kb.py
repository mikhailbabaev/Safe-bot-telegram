from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import TO_MAIN_MENU, REFERENCE, CHECK_SECURITY, PROMOCODE, UKASSA_PAYMENT



def promo_kb_success(price, wallet) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=UKASSA_PAYMENT.format(price=price), callback_data='url_ukassa')],
    [InlineKeyboardButton(text=REFERENCE.format(price=wallet), callback_data="reference")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])

promo_kb_wrong = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=PROMOCODE, callback_data="use_promocode")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])

promo_kb_activated = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=PROMOCODE, callback_data="use_promocode")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])
