from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import settings as cfg_settings
from keyboards import settings_keyboard
from messages import get_owner_id, set_owner_id
from states import SettingsStates

from .router import router


@router.callback_query(SettingsStates.edit_messages.choose_category, F.data == 'return_back')
@router.callback_query(SettingsStates.edit_admins.choose_action, F.data == 'return_back')
async def settings(callback: CallbackQuery, state: FSMContext) -> None:
    callback.answer()
    if not await get_owner_id():
        await set_owner_id(callback.from_user.id)
    if callback.from_user.id != await get_owner_id():
        return
    await callback.message.edit_text(
        cfg_settings.SETTINGS_MESSAGE,
        reply_markup=settings_keyboard,
    )
    await state.set_state(SettingsStates.choose_category)


@router.message(Command('settings'))
@router.message(CommandStart())
@router.message(F.text.lower().in_(cfg_settings.SETTINGS_HANDELR_RUN_MESSAGES))
async def settings(message: Message, state: FSMContext) -> None:
    if not await get_owner_id():
        await set_owner_id(message.from_user.id)
    if message.from_user.id != await get_owner_id():
        return
    await message.answer(
        cfg_settings.SETTINGS_MESSAGE,
        reply_markup=settings_keyboard,
    )
    await state.set_state(SettingsStates.choose_category)
