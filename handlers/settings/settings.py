from .router import router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F
from messages import get_owner_id, set_owner_id
from keyboards import settings_keyboard
from states import SettingsStates


@router.callback_query(SettingsStates.edit_messages.choose_category, F.data == 'return_back')
@router.callback_query(SettingsStates.edit_admins.choose_action, F.data == 'return_back')
async def settings(callback: CallbackQuery, state: FSMContext) -> None:
    if not await get_owner_id():
        await set_owner_id(callback.from_user.id)
    if callback.from_user.id != await get_owner_id():
        callback.answer('Отказано в доступе.')
        return
    await callback.message.edit_text(
        'Настройки:',
        reply_markup=settings_keyboard,
    )
    await state.set_state(SettingsStates.choose_category)


@router.message(Command('settings'))
@router.message(CommandStart())
@router.message(F.text == 'Настройки')
async def settings(message: Message, state: FSMContext) -> None:
    if not await get_owner_id():
        await set_owner_id(message.from_user.id)
    if message.from_user.id != await get_owner_id():
        return
    await message.answer(
        'Настройки:',
        reply_markup=settings_keyboard,
    )
    await state.set_state(SettingsStates.choose_category)
