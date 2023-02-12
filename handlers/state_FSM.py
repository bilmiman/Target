from aiogram.dispatcher.filters.state import StatesGroup, State


class Admins(StatesGroup):
    login = State()
    password = State()
    remember_me = State()

class give(StatesGroup):
    give_penalize = State()
    who_penalize = State()
    filial_penalize = State()
    who_bonus = State()
    filial_bonus = State()
    give_bonus = State()
    who_balance_check = State()
    filial_balance_check = State()


class add_employee(StatesGroup):
    add_fullname = State()
    add_date_of_birth = State()
    add_phone_number = State()
    add_region = State()
    add_job = State()
    add_take_to_work = State()
    add_filial = State()


class remove_employee(StatesGroup):
    remove_employee = State()
    filial = State()


class answers(StatesGroup):
    start = State()


class list(StatesGroup):
    list = State()

