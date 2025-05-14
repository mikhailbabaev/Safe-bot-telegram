import asyncio
import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from keyboards.common_keyboards import to_start_menu
from keyboards.checking_kb import (free_checking_menu,
                                   pay_checking_menu,
                                   get_step_action_kb,
                                   get_miss_action_kb,
                                   first_pay_check_kb)
from templates import (CHECKUP_TEXT,
                       CHECKUP_END,
                       PAY_CHECK_TEMPLATE,
                       END_PAY_CHECK,
                       FINALCHKUP_TEXT,
                       FINALCHKUP_END,
                       FAKECHECKUP_TEXT,
                       STEP_2,
                       STEP_3,
                       TRY_MISS_STEP)
from database.requests import (set_last_check_time,
                               set_user_action,
                               create_step_progress,
                               update_step_progress,
                               get_current_step,
                               get_step_progress,
                               delete_user_steps,
                               increase_user_achievement_number,
                               reset_user_achievements,
                               get_user_achievement_number,
                               get_user_check_text_number,
                               get_user_percent,
                               set_user_percent,
                               increase_user_percent_by_5,
                               get_user_payment_date,
                               set_user_percent_and_number)


check_router = Router()


async def delete_previous_message(callback: CallbackQuery, sleep_time: float = 1.5)-> None:
    tg_id = callback.from_user.id
    await callback.bot.send_chat_action(chat_id=tg_id, action="typing")
    await asyncio.sleep(sleep_time)
    await callback.message.delete()


def progress_bar(percent):
    """Декоративная шкала прогресса."""
    filled = "█" * (percent // 10)
    empty = "░" * (10 - percent // 10)
    return f"[{filled}{empty}] {percent}%"


async def show_step_1(message: Message, session: AsyncSession, kb, tg_id):
    await run_first_check(message=message, session=session, tg_id=tg_id)


async def show_step_2(message: Message, session: AsyncSession, kb, tg_id):
    await message.answer_video(video="CgACAgIAAxkBAAIHVmgMoO_XoH5WrDWU5RUdxg3cdpMPAAINeAACWT5pSJKTFp5i2y-NNgQ",
                               caption=STEP_2,
                               reply_markup=kb,
                               parse_mode="HTML")


async def show_step_3(message: Message, session: AsyncSession, kb, tg_id):
    await message.answer(text=STEP_3, reply_markup=kb, parse_mode="HTML")


STEP_FUNCTIONS = {
    "step_1": show_step_1,
    "step_2": show_step_2,
    "step_3": show_step_3,
}


async def show_step(message: Message, session: AsyncSession, step_id: str, tg_id: int):
    step_func = STEP_FUNCTIONS.get(step_id)
    if not step_func:
        await message.answer(text=END_PAY_CHECK)
    kb = get_step_action_kb(step_id)
    await step_func(message, session, kb, tg_id)



async def show_pay_check_menu(message: Message, chat_id: int, session: AsyncSession):
    await set_user_action(session, chat_id, 'pay_check_menu')
    payment_date = await get_user_payment_date(session, chat_id)

    text = PAY_CHECK_TEMPLATE.format(payment_date=payment_date.strftime('%d.%m.%Y %H:%M'))

    await message.answer(
        text=text,
        reply_markup=pay_checking_menu()
    )


async def checking_process(message: Message, tg_id: int, text: dict) -> None:
    """Имитация шагов проверки безопасности."""
    message = await message.answer(
        text="🔍 <b>Начинаем проверку безопасности аккаунта...</b>",
        parse_mode="HTML"
    )
    total_steps = len(text)
    progress_message = await message.answer(progress_bar(0))

    for i in range(1, total_steps + 1):
        progress = (i / total_steps) * 100
        await progress_message.edit_text(progress_bar(int(progress)))
        await asyncio.sleep(random.uniform(1.0, 2.5))
        await message.edit_text(text[i], parse_mode="HTML")

    await progress_message.delete()


async def run_security_check(message: Message, tg_id: int, session: AsyncSession, is_paid: bool = False):
    """Фиктивная проверка безопасности (бесплатная)."""
    await set_user_action(session, tg_id, 'free_check' if not is_paid else 'pay_check_action')
    user_text_number = await get_user_check_text_number(session, tg_id)
    user_percent = await get_user_percent(session, tg_id)
    if user_text_number is None or user_percent is None:
        user_percent = random.randint(40,65)
        user_text_number = random.randint(1, 3)
        await set_user_percent_and_number(session, tg_id, user_percent, user_text_number)
    if user_percent == 100:
        final_text = FINALCHKUP_END
    else:
        text_template = CHECKUP_END.get(user_text_number, CHECKUP_END[1])
        final_text = text_template.format(percent=user_percent)

    await checking_process(message, tg_id, FAKECHECKUP_TEXT)
    await set_last_check_time(session, tg_id)
    keyboard = pay_checking_menu() if is_paid else free_checking_menu
    await message.answer(final_text, reply_markup=keyboard, parse_mode="HTML")


async def run_first_check(message: Message, session: AsyncSession, tg_id: int):
    """Фиктивная проверка безопасности (платная)."""
    user_text_number = await get_user_check_text_number(session, tg_id)
    user_percent = await get_user_percent(session, tg_id)
    if user_text_number is None or user_percent is None:
        user_percent = random.randint(40,65)
        user_text_number = random.randint(1, 3)
        await set_user_percent_and_number(session, tg_id, user_percent, user_text_number)
    await checking_process(message, tg_id, CHECKUP_TEXT)
    text_template = CHECKUP_END.get(user_text_number, CHECKUP_END[1])
    final_text = text_template.format(percent=user_percent)
    await message.answer(final_text, parse_mode="HTML", reply_markup=first_pay_check_kb("step_1"))


async def run_final_check(message: Message, tg_id: int, session: AsyncSession):
    """Окончательная проверка безопасности (платная)."""
    await checking_process(message, tg_id, FINALCHKUP_TEXT)
    await message.answer(FINALCHKUP_END, parse_mode="HTML")
    await set_user_percent(session, tg_id, 100)


@check_router.callback_query(F.data == "check_security")
async def check_security(callback: CallbackQuery, session: AsyncSession):
    tg_id = callback.from_user.id
    now = datetime.now(timezone.utc)
    await callback.answer()
    payment_date = await get_user_payment_date(session, tg_id)
    is_paid = payment_date is not None and payment_date > now
    await run_security_check(callback.message, tg_id, session, is_paid)
    achivement = await get_user_achievement_number(session, tg_id)
    if achivement == 1:
        await increase_user_achievement_number(session, tg_id)


@check_router.callback_query(F.data == "paid_user")
async def handle_paid_user(callback: CallbackQuery, session: AsyncSession):
    await callback.answer()
    await show_pay_check_menu(callback.message, callback.from_user.id, session)


@check_router.callback_query(F.data == "pay_check")
async def handle_check_paid_user(callback: CallbackQuery, session: AsyncSession):
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'pay_check_action')
    current_step = await get_current_step(session, tg_id)
    await callback.answer()
    if current_step:
        progress = await get_step_progress(session, tg_id, current_step)
        if progress == "completed":
            await delete_user_steps(session, tg_id)
            await reset_user_achievements(session, tg_id)
            await set_user_percent(session, tg_id, None)
            await callback.message.answer("🔄 Вы уже прошли все шаги.\nПрогресс сброшен, начинаем заново.")
            current_step = "step_1"
            await create_step_progress(session, tg_id, current_step, status="started")
    if not current_step:
        current_step = "step_1"
        await create_step_progress(session, tg_id, current_step, status="started")
    await show_step(callback.message, session, current_step, tg_id)


@check_router.callback_query(F.data == "pay_check")
async def handle_check_paid_user(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'pay_check_action')
    print('1')
    current_step = await get_current_step(session, tg_id)
    print('2')
    if current_step:
        print('1')
        progress = await get_step_progress(session, tg_id, current_step)
        print('2')
        if progress == "completed":
            await delete_user_steps(session, tg_id)
            await reset_user_achievements(session, tg_id)
            await callback.message.answer("🔄 Вы уже прошли все шаги.\nПрогресс сброшен, начинаем заново.")
            current_step = "step_1"
            await create_step_progress(session, tg_id, current_step, status="started")
    if not current_step:
        current_step = "step_1"
        await create_step_progress(session, tg_id, current_step, status="started")
    await show_step(callback.message, session, current_step, tg_id)
    await callback.answer()


def get_next_step(current_step: str):
    steps = list(STEP_FUNCTIONS.keys())
    try:
        idx = steps.index(current_step)
        return steps[idx + 1] if idx + 1 < len(steps) else None
    except ValueError:
        return None


@check_router.callback_query(F.data.startswith("step_done:"))
async def handle_step_done(callback: CallbackQuery, session: AsyncSession):
    tg_id = callback.from_user.id
    step_id = callback.data.split(":")[1]
    await increase_user_percent_by_5(session, tg_id)
    await delete_previous_message(callback)

    await update_step_progress(session, tg_id, step_id, status="completed")
    await increase_user_achievement_number(session, tg_id)
    next_step = get_next_step(step_id)

    if next_step:
        await create_step_progress(session, tg_id, next_step, status="started")
        await show_step(callback.message, session, next_step, tg_id)
    else:
        await run_final_check(callback.message, tg_id, session)
        await callback.message.answer("🥳 Вы прошли все шаги! Ваш аккаунт максимально защищён.",
                                      reply_markup=to_start_menu)
    await callback.answer()


@check_router.callback_query(F.data.startswith("miss_step:"))
async def handle_more_info(callback: CallbackQuery):
    tg_id = callback.from_user.id
    step_id = callback.data.split(":")[1]
    await delete_previous_message(callback,
                                  sleep_time=0.5)

    await callback.message.answer(TRY_MISS_STEP,
                                  reply_markup=get_miss_action_kb(step_id),
                                  parse_mode="HTML")
    await callback.answer()


@check_router.callback_query(F.data.startswith("show_step:"))
async def handle_check_paid_user(callback: CallbackQuery, session: AsyncSession):
    step_id = callback.data.split(":")[1]
    tg_id = callback.from_user.id
    await delete_previous_message(callback, sleep_time=0)
    await show_step(callback.message, session, step_id, tg_id)
    await callback.answer()