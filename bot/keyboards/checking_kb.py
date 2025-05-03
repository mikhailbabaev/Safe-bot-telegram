from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from templates.buttons import PAYMENT, TO_MAIN_MENU, UKASSA_PAYMENT, PAY_CHECK


free_checking_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=PAYMENT, callback_data="payments")],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])


def first_pay_check_kb(current_step: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Устранить угрозу безопасности", callback_data=f'step_done:{current_step}')],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def pay_checking_menu(price) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=PAY_CHECK, callback_data="pay_check")],
    [InlineKeyboardButton(text=UKASSA_PAYMENT.format(price=price), callback_data='url_ukassa')],
    [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
])


def get_step_action_kb(current_step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сделал", callback_data=f"step_done:{current_step}")],
        [InlineKeyboardButton(text="ℹ️ Не хочу! Можно пропустить?", callback_data=f"miss_step:{current_step}")],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def get_info_action_kb(current_step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сделал", callback_data=f"step_done:{current_step}")],
        [InlineKeyboardButton(text="ℹ️ Не хочу! Можно пропустить?", callback_data=f"miss_step:{current_step}")],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])


def get_miss_action_kb(current_step: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Сделал", callback_data=f"step_done:{current_step}")],
        [InlineKeyboardButton(text="ℹ️ Инструкция", callback_data=f"show_step:{current_step}")],
        [InlineKeyboardButton(text=TO_MAIN_MENU, callback_data='go_to_start_menu')]
    ])