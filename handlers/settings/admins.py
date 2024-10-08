import asyncio

from aiogram import F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import admins_keyboard, return_back_keyboard
from messages import add_admin_id, get_admins_ids, get_owner_id, set_owner_id
from states import SettingsStates

from .router import router


async def deliting_admin() -> None:
    pass


@router.message(SettingsStates.edit_admins.add_admin)
async def add_admin(message: Message, state: FSMContext) -> None:
    # user = await message.bot.get_chat(message.text)
    callback = (await state.get_data())['callback']
    await state.clear()
    # user_link = f'https://t.me/{user.username}'
    # if user.id in await get_admins_ids():
    #     await admins(callback, state, f'*({user_link})[Пользователь]* уже является администратором.')
    #     return
    # await add_admin_id(user.id)
    await message.delete()
    await admins(callback, state, f'*Пользователь* теперь администратор.')


@router.callback_query(SettingsStates.edit_admins.choose_action, F.data == 'add_admin')
async def adding_admin(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.edit_text(
        'Для добавления администратора в бота отправьте мне его имя пользователя (@username)',
        reply_markup=return_back_keyboard,
    )
    await state.update_data(callback=callback)
    await state.set_state(SettingsStates.edit_admins.add_admin)


@router.callback_query(SettingsStates.choose_category, F.data == 'admins_settings')
@router.callback_query(SettingsStates.edit_admins.add_admin, F.data == 'return_back')
@router.callback_query(SettingsStates.edit_admins.delete_admin, F.data == 'return_back')
async def admins(callback: CallbackQuery, state: FSMContext, info: str = '') -> None:
    await callback.answer()
    admins = []
    for admin_id in await get_admins_ids():
        await asyncio.sleep(0)
        admin_user = (await callback.bot.get_chat_member(admin_id, admin_id)).user
        admin_username = admin_user.username
        if admin_username:
            admin_url = f'https://t.me/{admin_username}'
        else:
            admin_url = f'tg://openmessage?user_id={admin_id}'
        admins.append(f'({admin_url})[{admin_user.first_name}]')
    admins = '\n'.join(admins)
    info = f'{info}\n\n' if info else info
    await callback.message.edit_text(
        f'{info}Действующие администраторы в боте:\n{admins}\n\nВыберите действие:',
        reply_markup=admins_keyboard,
        parse_mode=ParseMode.MARKDOWN,
    )
    await state.set_state(SettingsStates.edit_admins.choose_action)