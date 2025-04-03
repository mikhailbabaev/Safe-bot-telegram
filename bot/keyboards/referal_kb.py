from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import COPY_PROMOCODE, WITHDRAW_MONEY, TO_MAIN_MENU

referal_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=COPY_PROMOCODE, callback_data="copy_promocode")],
    [InlineKeyboardButton(text=WITHDRAW_MONEY, callback_data="withdraw_money")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])

referal_getout_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])