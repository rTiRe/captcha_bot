from .router import router
from aiogram import F
from states import SettingsStates
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import message_edit_keyboard
from aiogram.utils.serialization import deserialize_telegram_object_to_python


@router.callback_query(
    SettingsStates.edit_messages.choose_category,
    F.data == 'edit_captcha_button',
)
async def edit_captcha_button(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        'Отправьте новый текст кнопки капчи (оставьте пустым, чтобы не отображать):',
        reply_markup=message_edit_keyboard,
    )
    await state.update_data(callback=callback, message_type='captcha_buttons')
    await state.set_state(SettingsStates.edit_messages.edit_captcha_button)
    await callback.answer()