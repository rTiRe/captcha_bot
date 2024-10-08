from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import settings

back_button = InlineKeyboardButton(
    text=settings.RETURN_BACK_BUTTON,
    callback_data='return_back',
)

settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(
    #   text=settings.ADMINS_BUTTON,
    #   callback_data='admins_settings',
    # )],
    [InlineKeyboardButton(
        text=settings.MESSAGES_BUTTON,
        callback_data='messages_settigs',
    )],
])


admins_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
    [InlineKeyboardButton(
        text=settings.ADD_ADMIN_BUTTON,
        callback_data='add_admin',
    )],
    [InlineKeyboardButton(
        text=settings.REMOVE_ADMIN_BUTTON,
        callback_data='remove_admin',
    )],
])


edit_messages_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
    [InlineKeyboardButton(
        text=settings.EDIT_HELLO_MESSAGE_BUTTON,
        callback_data='edit_hello',
    )],
    [InlineKeyboardButton(
        text=settings.EDIT_CAPTCHA_MESSAGE_BUTTON,
        callback_data='edit_captcha',
    )],
    [InlineKeyboardButton(
        text=settings.EDIT_CAPTCHA_BUTTON_BUTTON,
        callback_data='edit_captcha_button',
    )],
    [InlineKeyboardButton(
        text=settings.EDIT_WELCOME_MESSAGE_BUTTON,
        callback_data='edit_welcome',
    )],
])

return_back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
])

message_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
    [InlineKeyboardButton(
        text=settings.LEAVE_BLANK_BUTTON,
        callback_data='blank',
    )],
])
