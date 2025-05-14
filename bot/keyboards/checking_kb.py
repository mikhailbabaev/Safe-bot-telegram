from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import PAYMENT, TO_MAIN_MENU, UKASSA_PAYMENT, PAY_CHECK, DONE, DONT_DO


free_checking_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=PAYMENT, callback_data="payments")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])


def first_pay_check_kb(current_step: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Устранить угрозу безопасности", callback_data=f'step_done:{current_step}')],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def pay_checking_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=PAY_CHECK, callback_data="pay_check")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])


def get_step_action_kb(current_step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=DONE, callback_data=f"step_done:{current_step}")],
        [InlineKeyboardButton(text=DONT_DO, callback_data=f"miss_step:{current_step}")],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def get_info_action_kb(current_step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=DONE, callback_data=f"step_done:{current_step}")],
        [InlineKeyboardButton(text=DONT_DO, callback_data=f"miss_step:{current_step}")],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def get_miss_action_kb(current_step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ Вернуться к инструкции", callback_data=f"show_step:{current_step}")],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])