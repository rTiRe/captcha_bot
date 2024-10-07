from aiogram.fsm.state import State, StatesGroup

class CaptchaStates(StatesGroup):
    waiting_captcha = State()


class EditingAdminsStates(StatesGroup):
    choose_action = State()
    add_admin = State()
    delete_admin = State()


class EditingMessagesStates(StatesGroup):
    choose_category = State()
    edit_hello_message = State()
    edit_captcha_message = State()
    edit_captcha_button = State()
    edit_welcome_message = State()


class SettingsStates(StatesGroup):
    choose_category = State()
    edit_admins = EditingAdminsStates
    edit_messages = EditingMessagesStates
