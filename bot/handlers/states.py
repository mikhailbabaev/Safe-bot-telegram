from aiogram.fsm.state import StatesGroup, State

class MyStates(StatesGroup):
    waiting_for_input = State()
