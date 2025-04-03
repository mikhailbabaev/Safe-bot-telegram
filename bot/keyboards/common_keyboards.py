from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import FAQ, PAYMENT, REFERENCE, CHECK_SECURITY, ACHIVEMENTS, TO_MAIN_MENU

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=CHECK_SECURITY, callback_data="check_security")],
    [InlineKeyboardButton(text=PAYMENT, callback_data="payments")],
    [InlineKeyboardButton(text=REFERENCE, callback_data="cashback")],
    [InlineKeyboardButton(text=ACHIVEMENTS, callback_data='achivements')],
    [InlineKeyboardButton(text=FAQ, callback_data="FAQ")]
])


to_start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])

