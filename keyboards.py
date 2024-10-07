from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_button = InlineKeyboardButton(text='Назад', callback_data='return_back')

settings_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(text='Администраторы', callback_data='admins_settings')],
    [InlineKeyboardButton(text='Сообщения', callback_data='messages_settigs')],
])


admins_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
    [InlineKeyboardButton(text='Добавить админа', callback_data='add_admin')],
    [InlineKeyboardButton(text='Удалить админа', callback_data='remove_admin')],
])


edit_messages_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
    [InlineKeyboardButton(text='Приветствие бота', callback_data='edit_hello')],
    [InlineKeyboardButton(text='Сообщение капчи', callback_data='edit_captcha')],
    [InlineKeyboardButton(text='Кнопка капчи', callback_data='edit_captcha_button')],
    [InlineKeyboardButton(text='Приветствие канала', callback_data='edit_welcome')],
])

return_back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
])

message_edit_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [back_button],
    [InlineKeyboardButton(text='Оставить пустым', callback_data='blank')],
])
