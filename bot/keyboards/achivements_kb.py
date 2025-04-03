from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import TO_MAIN_MENU, CHECK_SECURITY

achive_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=CHECK_SECURITY, callback_data="check_security")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data="go_to_start_menu")],
])
