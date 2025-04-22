from aiogram.fsm.state import StatesGroup, State

class MyStates(StatesGroup):
    waiting_for_input = State()


class PaymentState(StatesGroup):
    waiting_for_payment = State()