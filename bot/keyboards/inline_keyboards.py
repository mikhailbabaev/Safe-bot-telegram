from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import FAQ, PAYMENT, REFERENCE, CHECK_SECURITY, TO_MAIN_MENU, UKASSA_PAYMENT

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=CHECK_SECURITY, callback_data="check_security")],
    [InlineKeyboardButton(text=PAYMENT, callback_data="payments")],
    [InlineKeyboardButton(text=REFERENCE, callback_data="reference")],
    [InlineKeyboardButton(text=FAQ, callback_data="FAQ")]
])


FAQ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])


payments = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=UKASSA_PAYMENT, callback_data='pay_to_ukassa')],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])