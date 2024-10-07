from .router import router
from aiogram import F
from states import SettingsStates
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards import message_edit_keyboard

@router.callback_query(
    SettingsStates.edit_messages.choose_category,
    F.data == 'edit_welcome',
)
async def edit_welcome_message(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        'Отправьте новое сообщение приветствия канала (оставьте пустым, чтобы не отображать):',
        reply_markup=message_edit_keyboard,
    )
    await state.update_data(callback=callback, message_type='welcome_messages')
    await state.set_state(SettingsStates.edit_messages.edit_welcome_message)
    await callback.answer()