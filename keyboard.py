from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приветствие бота', callback_data='edit_welcome')],
    [InlineKeyboardButton(text='Сообщение капчи', callback_data='edit_captcha')],
    [InlineKeyboardButton(text='Кнопка капчи', callback_data='edit_captcha_button')],
    [InlineKeyboardButton(text='Приветка канала', callback_data='edit_hello')],
])

editor_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='return_back')],
    [InlineKeyboardButton(text='Оставить пустым', callback_data='blank')],
])

