from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import PAYMENT, TO_MAIN_MENU, ACHIVEMENTS


checking_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=PAYMENT, callback_data="payments")],
    [InlineKeyboardButton(text=ACHIVEMENTS, callback_data='achivements')],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])
