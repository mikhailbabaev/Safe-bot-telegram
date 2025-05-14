from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import FAQ, PAYMENT, REFERENCE, CHECK_SECURITY, ACHIVEMENTS, TO_MAIN_MENU


to_start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])


def get_start_menu(achievement_text: str, is_paid: bool, wallet: int) -> InlineKeyboardMarkup:
    payments_callback = "paid_user" if is_paid else "payments"
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=CHECK_SECURITY, callback_data="check_security")],
        [InlineKeyboardButton(text=PAYMENT, callback_data=payments_callback)],
        [InlineKeyboardButton(text=REFERENCE.format(wallet=wallet), callback_data="cashback")],
        [InlineKeyboardButton(text=achievement_text, callback_data="achivements")],
        [InlineKeyboardButton(text=FAQ, callback_data="FAQ")]
    ])