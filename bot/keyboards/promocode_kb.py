from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import TO_MAIN_MENU, REFERENCE, CHECK_SECURITY, PROMOCODE, UKASSA_PAYMENT


promo_kb_success = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=UKASSA_PAYMENT, callback_data="url_ukassa")],
    [InlineKeyboardButton(text=REFERENCE, callback_data="reference")],
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
