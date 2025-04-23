import asyncio
import random

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards.common_keyboards import to_start_menu
from keyboards.checking_kb import (free_checking_menu,
                                   pay_checking_menu,
                                   get_step_action_kb,
                                   get_info_action_kb,
                                   get_miss_action_kb)
from templates import (CHECKUP_TEXT,
                       CHECKUP_END,
                       PAY_CHECK_TEMPLATE,
                       STEP_TEXTS,
                       END_PAY_CHECK,
                       FINALCHKUP_TEXT,
                       FINALCHKUP_END,
                       FAKECHECKUP_END,
                       FAKECHECKUP_TEXT,
                       )
from database.requests import (set_last_check_time,
                               set_user_action,
                               get_user_payment_date,
                               create_step_progress,
                               update_step_progress,
                               get_current_step,
                               get_step_progress,
                               delete_user_steps,
                               increase_user_achievement_number,
                               reset_user_achievements)


check_router = Router()


async def delete_previous_message(callback: CallbackQuery, text: str = "", sleep_time: float = 1.5)-> None:
    tg_id = callback.from_user.id
    await callback.bot.send_chat_action(chat_id=tg_id, action="typing")
    if text:
        await callback.message.edit_text(text)
        await asyncio.sleep(sleep_time)
    await callback.message.delete()


async def send_typing_effect(message: Message, text_blocks: dict, delay: float = 1.0):
    """Функция для постепенной отправки текста, сохраняя форматирование и обновляя одно сообщение"""
    sent_message = await message.answer("Загрузка...", parse_mode="HTML")

    for key in sorted(text_blocks.keys()):
        full_text = "\n".join(list(text_blocks.values())[:key])
        await sent_message.edit_text(full_text.strip(), parse_mode="HTML")
        await asyncio.sleep(delay)


def progress_bar(percent):
    """Декоративная шкала прогресса."""
    filled = "█" * (percent // 10)
    empty = "░" * (10 - percent // 10)
    return f"[{filled}{empty}] {percent}%"


async def show_step(message: Message, step_id: str):
    if step_id not in STEP_TEXTS:
        await message.answer(
            text=END_PAY_CHECK,
        )
        return

    text = STEP_TEXTS[step_id]
    kb = get_step_action_kb(step_id)
    await message.answer(text=text, reply_markup=kb)


async def show_pay_check_menu(bot: Bot, chat_id: int, session: AsyncSession):
    await set_user_action(session, chat_id, 'pay_check_menu')
    payment_date = await get_user_payment_date(session, chat_id)

    text = (
        f"✅ Ваша подписка активна до: {payment_date.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"{PAY_CHECK_TEMPLATE}"
    )

    keyboard = pay_checking_menu

    await bot.send_message(
        chat_id,
        text=text,
        reply_markup=keyboard
    )


async def checking_process(bot: Bot, tg_id: int, text: dict) -> None:
    """Имитация шагов проверки безопасности."""
    message = await bot.send_message(tg_id, "Начинаем проверку безопасности...")
    total_steps = len(text)
    progress_message = await bot.send_message(tg_id, progress_bar(0))

    for i in range(1, total_steps + 1):
        progress = (i / total_steps) * 100
        await progress_message.edit_text(progress_bar(int(progress)))
        await asyncio.sleep(random.uniform(1.0, 2.5))
        await message.edit_text(text[i])

    await progress_message.delete()


async def run_security_check(bot: Bot, tg_id: int, session: AsyncSession, is_paid: bool = False):
    """Фиктивная проверка безопасности (бесплатная)."""
    await set_user_action(session, tg_id, 'free_check' if not is_paid else 'pay_check_action')

    await checking_process(bot, tg_id, FAKECHECKUP_TEXT)
    await set_last_check_time(session, tg_id)
    await increase_user_achievement_number(session, tg_id)
    keyboard = pay_checking_menu if is_paid else free_checking_menu
    await bot.send_message(tg_id, FAKECHECKUP_END, reply_markup=keyboard)


async def run_first_check(bot: Bot, tg_id: int):
    """Фиктивная проверка безопасности (платная)."""
    await checking_process(bot, tg_id, CHECKUP_TEXT)
    await bot.send_message(tg_id, CHECKUP_END, parse_mode="Markdown")


async def run_final_check(bot: Bot, tg_id: int):
    """Окончательная проверка безопасности (бесплатная)."""
    await checking_process(bot, tg_id, FINALCHKUP_TEXT)
    await bot.send_message(tg_id, FINALCHKUP_END)


@check_router.callback_query(F.data == "check_security")
async def check_security(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    await run_security_check(callback.bot, callback.from_user.id, session, is_paid=False)


@check_router.callback_query(F.data == "paid_user")
async def handle_paid_user(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    await show_pay_check_menu(callback.bot, callback.from_user.id, session)


@check_router.callback_query(F.data == "pay_check")
async def handle_check_paid_user(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'pay_check_action')
    current_step = await get_current_step(session, tg_id)

    if current_step:
        progress = await get_step_progress(session, tg_id, current_step)
        if progress == "completed":
            await delete_user_steps(session, tg_id)
            await reset_user_achievements(session, tg_id)
            await callback.message.answer("🔄 Вы уже прошли все шаги.\nПрогресс сброшен, начинаем заново.")
            current_step = "step_1"
            await create_step_progress(session, tg_id, current_step, status="started")
    if not current_step:
        current_step = "step_1"
        await create_step_progress(session, tg_id, current_step, status="started")

    if current_step == "step_1":
        await run_first_check(callback.bot, tg_id)

    await show_step(callback.message, current_step)
    await callback.answer()


def get_next_step(current_step: str):
    steps = list(STEP_TEXTS.keys())
    try:
        idx = steps.index(current_step)
        return steps[idx + 1] if idx + 1 < len(steps) else None
    except ValueError:
        return None


@check_router.callback_query(F.data.startswith("step_done:"))
async def handle_step_done(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    tg_id = callback.from_user.id
    step_id = callback.data.split(":")[1]

    await delete_previous_message(callback, text="🕵️‍♂️️ Проверяем, как вы улучшили свою безопасность...")

    await update_step_progress(session, tg_id, step_id, status="completed")
    await increase_user_achievement_number(session, tg_id)
    next_step = get_next_step(step_id)

    if next_step:
        await create_step_progress(session, tg_id, next_step, status="started")
        await show_step(callback.message, next_step)
    else:
        await run_final_check(callback.bot, tg_id)
        await callback.message.answer("🥳 Вы прошли все шаги! Ваш аккаунт максимально защищён.",
                                      reply_markup=to_start_menu)
    await callback.answer()


@check_router.callback_query(F.data.startswith("step_info:"))
async def handle_more_info(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    step_id = callback.data.split(":")[1]
    await delete_previous_message(callback, text="", sleep_time=0.5)

    await callback.message.answer(f"ℹ️ Подробная информация по шагу: {step_id}\n\n"
                                  f"(Тут будет описание или советы по выполнению)",
                                  reply_markup=get_info_action_kb(step_id))
    await callback.answer()


@check_router.callback_query(F.data.startswith("miss_step:"))
async def handle_more_info(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id
    step_id = callback.data.split(":")[1]
    await delete_previous_message(callback,
                                  text="",
                                  sleep_time=0.5)

    await callback.message.answer(f"ℹ️ Нельзя пропустить, ваша безопасность стоит одной минутки: \n\n"
                                  f"К тому же думать полезно\n\n"
                                  f"Выполните шаг {step_id} позязя)",
                                  reply_markup=get_miss_action_kb(step_id))
    await callback.answer()