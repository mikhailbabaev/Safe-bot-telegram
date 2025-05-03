import asyncio
import random

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from keyboards.common_keyboards import to_start_menu
from keyboards.checking_kb import (free_checking_menu,
                                   pay_checking_menu,
                                   get_step_action_kb,
                                   get_info_action_kb,
                                   get_miss_action_kb,
                                   first_pay_check_kb)
from templates import (CHECKUP_TEXT,
                       CHECKUP_END,
                       PAY_CHECK_TEMPLATE,
                       END_PAY_CHECK,
                       FINALCHKUP_TEXT,
                       FINALCHKUP_END,
                       FAKECHECKUP_END,
                       FAKECHECKUP_TEXT,
                       STEP_1,
                       STEP_2,
                       STEP_3,)
from database.requests import (set_last_check_time,
                               set_user_action,
                               get_user_payment_date,
                               create_step_progress,
                               update_step_progress,
                               get_current_step,
                               get_step_progress,
                               delete_user_steps,
                               increase_user_achievement_number,
                               reset_user_achievements,
                               get_user_achievement_number,
                               get_user_check_text_number,
                               set_user_check_number,
                               get_user_percent,
                               set_user_percent,
                               check_promocode_is_active,
                               increase_user_percent_by_5,
                               get_user_payment_date)


check_router = Router()


async def delete_previous_message(callback: CallbackQuery, text: str = "", sleep_time: float = 1.5)-> None:
    tg_id = callback.from_user.id
    await callback.bot.send_chat_action(chat_id=tg_id, action="typing")
    await asyncio.sleep(sleep_time)
    await callback.message.delete()


def progress_bar(percent):
    """Декоративная шкала прогресса."""
    filled = "█" * (percent // 10)
    empty = "░" * (10 - percent // 10)
    return f"[{filled}{empty}] {percent}%"


async def show_step_1(message: Message, session: AsyncSession, kb):
    tg_id=message.from_user.id
    await run_first_check(message=message, session=session, tg_id=tg_id)
    await message.answer(text=STEP_1, reply_markup=kb)


async def show_step_2(message: Message, session: AsyncSession, kb):
    await message.answer_video(video="CgACAgIAAxkBAAIHVmgMoO_XoH5WrDWU5RUdxg3cdpMPAAINeAACWT5pSJKTFp5i2y-NNgQ",
                               caption=STEP_2,
                               reply_markup=kb)


async def show_step_3(message: Message, session: AsyncSession, kb):
    await message.answer(text=STEP_3, reply_markup=kb)


STEP_FUNCTIONS = {
    "step_1": show_step_1,
    "step_2": show_step_2,
    "step_3": show_step_3,
}


async def show_step(message: Message, session: AsyncSession, step_id: str):
    step_func = STEP_FUNCTIONS.get(step_id)
    if not step_func:
        await message.answer(text=END_PAY_CHECK)
    kb = get_step_action_kb(step_id)
    await step_func(message, session, kb)



async def show_pay_check_menu(message: Message, chat_id: int, session: AsyncSession):
    await set_user_action(session, chat_id, 'pay_check_menu')
    payment_date = await get_user_payment_date(session, chat_id)

    text = (
        f"✅ Ваша подписка активна до: {payment_date.strftime('%d.%m.%Y %H:%M')}\n\n"
        f"{PAY_CHECK_TEMPLATE}"
    )
    price = 149 if await check_promocode_is_active(session, chat_id) else 199

    await message.answer(
        text=text,
        reply_markup=pay_checking_menu(price)
    )


async def checking_process(message: Message, tg_id: int, text: dict) -> None:
    """Имитация шагов проверки безопасности."""
    message = await message.answer(text="Начинаем проверку безопасности...")
    total_steps = len(text)
    progress_message = await message.answer(progress_bar(0))

    for i in range(1, total_steps + 1):
        progress = (i / total_steps) * 100
        await progress_message.edit_text(progress_bar(int(progress)))
        await asyncio.sleep(random.uniform(1.0, 2.5))
        await message.edit_text(text[i])

    await progress_message.delete()


async def run_security_check(message: Message, tg_id: int, session: AsyncSession, is_paid: bool = False):
    """Фиктивная проверка безопасности (бесплатная)."""
    await set_user_action(session, tg_id, 'free_check' if not is_paid else 'pay_check_action')
    user_text_number = await get_user_check_text_number(session, tg_id)
    user_percent = await get_user_percent(session, tg_id)
    if user_text_number is None or user_percent is None:
        user_percent = random.randint(40,65)
        user_text_number = random.randint(1, 3)
        await set_user_percent(session, tg_id, user_percent)
        await set_user_check_number(session,tg_id, user_text_number)

    text_template = CHECKUP_END.get(user_text_number, CHECKUP_END[1])
    final_text = text_template.format(percent=user_percent)
    print(f'фиктивная проверка {user_percent}, {is_paid}')
    print(f"user_text_number = {user_text_number}, user_percent = {type(user_percent)}" )

    await checking_process(message, tg_id, FAKECHECKUP_TEXT)
    await set_last_check_time(session, tg_id)
    price = 149 if await check_promocode_is_active(session, tg_id) else 199
    keyboard = pay_checking_menu(price) if is_paid else free_checking_menu
    await message.answer(final_text, reply_markup=keyboard)


async def run_first_check(message: Message, session: AsyncSession, tg_id: int):
    """Фиктивная проверка безопасности (платная)."""
    user_text_number = await get_user_check_text_number(session, tg_id)
    user_percent = await get_user_percent(session, tg_id)
    if not user_text_number and not user_percent:
        user_percent = random.randint(40,65)
        user_text_number = random.randint(1, 3)
        await set_user_percent(session, tg_id, user_percent)
        await set_user_check_number(session,tg_id, user_text_number)
    await checking_process(message, tg_id, CHECKUP_TEXT)
    text_template = CHECKUP_END.get(user_text_number, CHECKUP_END[1])
    final_text = text_template.format(percent=user_percent)
    await message.answer(final_text, parse_mode="Markdown", reply_markup=first_pay_check_kb("step_1"))


async def run_final_check(message: Message, tg_id: int, session: AsyncSession):
    """Окончательная проверка безопасности (платная)."""
    await checking_process(message, tg_id, FINALCHKUP_TEXT)
    await message.answer(FINALCHKUP_END)
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
async def handle_check_paid_user(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    tg_id = callback.from_user.id
    await set_user_action(session, tg_id, 'pay_check_action')
    # проверяем, на каком шаге юзер
    current_step = await get_current_step(session, tg_id)
    # если шагов нет, создаем и действуем по порядку
    # шаг 1 - провести проверку и перейти к шагу два
    # шаг два - рекомендовать провести 2FA и проверить активные сессии
    # шаг три повторная проверка
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
    # если шаги есть, то проверяем прогресс последнего шага
    await show_step(callback.message, session, current_step)
    # если последний шаг "completed" то все шаги завершены и мы обнуляем проверку
    await callback.answer()


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
    await delete_previous_message(callback, text="🕵️‍♂️️ Проверяем, как вы улучшили свою безопасность...")

    await update_step_progress(session, tg_id, step_id, status="completed")
    await increase_user_achievement_number(session, tg_id)
    next_step = get_next_step(step_id)

    if next_step:
        await create_step_progress(session, tg_id, next_step, status="started")
        await show_step(callback.message, session, next_step)
    else:
        await run_final_check(callback.message, tg_id, session)
        await callback.message.answer("🥳 Вы прошли все шаги! Ваш аккаунт максимально защищён.",
                                      reply_markup=to_start_menu)
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


@check_router.callback_query(F.data.startswith("show_step:"))
async def handle_check_paid_user(callback: CallbackQuery, session: AsyncSession):
    step_id = callback.data.split(":")[1]
    tg_id = callback.from_user.id
    await delete_previous_message(callback, sleep_time=0)
    await show_step(callback.message, session, step_id)
    await callback.answer()