from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import settings
from keyboards import message_edit_keyboard
from states import SettingsStates

from .router import router


@router.callback_query(
    SettingsStates.edit_messages.choose_category,
    F.data == 'edit_captcha',
)
async def edit_captcha_message(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        settings.NEW_CAPTCHA_MESSAGE_MESSAGE,
        reply_markup=message_edit_keyboard,
    )
    await state.update_data(callback=callback, message_type='captcha_messages')
    await state.set_state(SettingsStates.edit_messages.edit_captcha_message)
    await callback.answer()