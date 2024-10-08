from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TOKEN: str

    @property
    def db_url(self) -> str:
        return f'sqlite+aiosqlite:///db.sqlite'

    class Config:
        env_file = 'config/.env'


settings = Settings()

JOIN_REQUEST_TIMEOUT = 90

# Keyboard
RETURN_BACK_BUTTON = '◀️ назад'
ADMINS_BUTTON = '🛡️ Администраторы'
MESSAGES_BUTTON = '💬 Сообщения'
ADD_ADMIN_BUTTON = '➕ Добавить админа'
REMOVE_ADMIN_BUTTON = '➖ Удалить админа'
EDIT_HELLO_MESSAGE_BUTTON = '👋 Приветствие бота'
EDIT_CAPTCHA_MESSAGE_BUTTON = '🔏 Сообщение капчи'
EDIT_CAPTCHA_BUTTON_BUTTON = '🔐 Кнопка капчи'
EDIT_WELCOME_MESSAGE_BUTTON = '🔓 Приветствие канала'
LEAVE_BLANK_BUTTON = '✖️ Оставить пустым'

# Settings
CHOOSE_CATEGORY_MESSAGE = '{info}Выберите категорию для редактирования:'
SETTINGS_HANDELR_RUN_MESSAGES = ('настройки', 'settings')
SETTINGS_MESSAGE = '⚙️ Настройки:'
NEW_HELLO_MESSAGE_MESSAGE = 'Отправьте новое сообщение приветствия бота (оставьте пустым, чтобы не отображать):'
NEW_CAPTCHA_MESSAGE_MESSAGE = 'Отправьте новое сообщение капчи (оставьте пустым, чтобы не отображать):'
NEW_CAPTCHA_BUTTON_MESSAGE = 'Отправьте новый текст кнопки капчи (оставьте пустым, чтобы не отображать):'
NEW_WELCOME_MESSAGE_MESSAGE = 'Отправьте новое сообщение приветствия канала (оставьте пустым, чтобы не отображать):'
SUCCESS_EDITED_INFO = '✅ *Успешно* изменено.'
EDITING_ERROR_INFO = '❌ *Ошибка* изменения сообщения.'
