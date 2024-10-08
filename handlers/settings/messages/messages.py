from aiogram import F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.serialization import deserialize_telegram_object_to_python

from config import settings
from keyboards import edit_messages_keyboard
from messages import set_message
from states import SettingsStates

from .router import router


@router.message(SettingsStates.edit_messages.edit_hello_message)
@router.message(SettingsStates.edit_messages.edit_captcha_button)
@router.message(SettingsStates.edit_messages.edit_captcha_message)
@router.message(SettingsStates.edit_messages.edit_welcome_message)
@router.message(SettingsStates.edit_messages.edit_timeout_message)
async def edit_message(message: Message, state: FSMContext, query: CallbackQuery = None) -> None:
    state_data = await state.get_data()
    callback: CallbackQuery = state_data['callback']
    message_type: str = state_data['message_type']
    message_json = deserialize_telegram_object_to_python(message)
    if query:
        added_by = query.from_user.id
    else:
        added_by = message.from_user.id
    try:
        await set_message(message_type, message_json, added_by, is_active=True)
    except:
        info = settings.EDITING_ERROR_INFO
    else:
        info = settings.SUCCESS_EDITED_INFO
    finally:
        if message: await message.delete()
        await state.clear()
        await messages(callback, state, info)


@router.callback_query(SettingsStates.edit_messages.edit_hello_message, F.data == 'blank')
@router.callback_query(SettingsStates.edit_messages.edit_captcha_button, F.data == 'blank')
@router.callback_query(SettingsStates.edit_messages.edit_captcha_message, F.data == 'blank')
@router.callback_query(SettingsStates.edit_messages.edit_welcome_message, F.data == 'blank')
@router.callback_query(SettingsStates.edit_messages.edit_timeout_message, F.data == 'blank')
async def leave_blank(query: CallbackQuery, state: FSMContext) -> None:
    await edit_message('', state, query)


@router.callback_query(SettingsStates.choose_category, F.data == 'messages_settigs')
@router.callback_query(SettingsStates.edit_messages.edit_hello_message, F.data == 'return_back')
@router.callback_query(SettingsStates.edit_messages.edit_captcha_button, F.data == 'return_back')
@router.callback_query(SettingsStates.edit_messages.edit_captcha_message, F.data == 'return_back')
@router.callback_query(SettingsStates.edit_messages.edit_welcome_message, F.data == 'return_back')
@router.callback_query(SettingsStates.edit_messages.edit_timeout_message, F.data == 'return_back')
async def messages(callback: CallbackQuery, state: FSMContext, info: str = '') -> None:
    info = f'{info}\n\n' if info else info
    await callback.message.edit_text(
        settings.CHOOSE_CATEGORY_MESSAGE.format(info=info),
        reply_markup=edit_messages_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(SettingsStates.edit_messages.choose_category)
    try:
        await callback.answer()
    except TelegramBadRequest:
        return