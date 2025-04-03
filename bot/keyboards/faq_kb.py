from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from templates.buttons import TO_MAIN_MENU


FAQ = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])
