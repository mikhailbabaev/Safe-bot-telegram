from aiogram.fsm.state import StatesGroup, State

class MyStates(StatesGroup):
    waiting_for_input = State()
    waiting_for_menu_update = State()