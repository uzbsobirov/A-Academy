from aiogram.filters.state import StatesGroup, State


class Test(StatesGroup):
    Q1 = State()
    Q2 = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
    main = State()
    statistic = State()
    sponsors = State()
    get_channel = State()
    delete_sponsor = State()
    admins = State()
    adding_admin = State()
    delete_admin = State()
    test_set = State()
    get_code = State()
    ball = State()
    get_answers = State()
    cancel = State()
