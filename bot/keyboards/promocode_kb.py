from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import TO_MAIN_MENU, REFERENCE, CHECK_SECURITY


promo_kb_enter = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])

promo_kb_success = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=CHECK_SECURITY, callback_data="check_security")],
    [InlineKeyboardButton(text=REFERENCE, callback_data="check_security")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])

promo_kb_wrong = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=CHECK_SECURITY, callback_data="check_security")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])

promo_kb_activated = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=CHECK_SECURITY, callback_data="check_security")],
    [InlineKeyboardButton(text=REFERENCE, callback_data='reference')],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])
