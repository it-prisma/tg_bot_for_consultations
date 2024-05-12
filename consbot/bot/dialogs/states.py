from aiogram.fsm.state import State, StatesGroup


class StartMenuSG(StatesGroup):
    menu = State()


class RegisterRegularSG(StatesGroup):
    input_name = State()
    gender_pronouns = State()


class RegisterConsultantSG(StatesGroup):
    input_name = State()
    gender_pronouns = State()
    choose_include_themes = State()
    choose_exclude_themes = State()
    confirmation = State()


class ConsultantPendingSG(StatesGroup):
    wait = State()
