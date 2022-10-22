from aiogram.dispatcher.filters.state import State, StatesGroup



class Mailing(StatesGroup):
    waitText = State()


class ChangePercent(StatesGroup):
    waitPercent = State()


class ChangeRequisites(StatesGroup):
    waitRequisites = State()