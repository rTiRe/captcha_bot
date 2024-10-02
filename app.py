from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import ChatJoinRequest, CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import aiofiles

from dotenv import load_dotenv
from os import getenv
import asyncio
import logging
import json
from keyboard import keyboard, editor_keyboard

logging.basicConfig(level=logging.INFO)

load_dotenv()

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher()

messages: dict
with open('messages.json', 'r') as file:
    messages = json.load(file)


class Edit(StatesGroup):
    edit = State()


async def background() -> None:
    while True:
        await asyncio.sleep(0)


async def get_message(message_name: str, request: CallbackQuery | ChatJoinRequest) -> str:
    return messages[message_name].format(
        user_full_name=request.from_user.full_name,
        user_first_name=request.from_user.first_name,
        user_last_name=request.from_user.last_name,
        channel_name=r'{channel_name}',
    )


@dp.callback_query(F.data.split(',')[0] == 'approve' and F.data.split(',').len() == 2)
async def approve(callback: CallbackQuery) -> None:
    await callback.answer()
    hello_message = (await get_message('hello', callback)).format(
        channel_name=(await bot.get_chat(callback.data.split(',')[1])).full_name,
    )
    if hello_message:
        await callback.message.edit_text(
            hello_message,
            parse_mode=ParseMode.MARKDOWN,
        )
    await bot.approve_chat_join_request(
        callback.data.split(',')[1],
        callback.from_user.id,
    )


@dp.chat_join_request()
async def captcha(request: ChatJoinRequest) -> None:
    welcome_message = (await get_message('welcome', request)).format(
        channel_name=request.chat.full_name,
    )
    if welcome_message:
        await bot.send_message(
            request.from_user.id,
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
        )
    captcha_message = await get_message('captcha', request)
    captcha_button = await get_message('captcha_button', request)
    if captcha_button and captcha_message:
        keyboard = InlineKeyboardBuilder()
        keyboard.add(InlineKeyboardButton(text=captcha_button, callback_data=f'approve,{request.chat.id}'))
        await bot.send_message(
            request.from_user.id,
            captcha_message,
            reply_markup=keyboard.as_markup(),
            parse_mode=ParseMode.MARKDOWN,
        )


@dp.message(Edit.edit)
async def new_message(message: Message, state: FSMContext) -> None:
    if message.from_user.id != int(messages['owner_id']):
        return
    data = await state.get_data()
    await state.clear()
    messages[data['edit']] = message.text
    messages_str = json.dumps(messages, ensure_ascii=False, indent=4)
    async with aiofiles.open('messages.json', 'w') as file:
        await file.write(messages_str)
    await message.delete()
    answer = await message.answer('Успешно изменено!')
    await return_back(data['callback'], state)
    await asyncio.sleep(1)
    await answer.delete()



@dp.callback_query(F.data == 'return_back')
async def return_back(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.from_user.id != int(messages['owner_id']):
        return
    await callback.answer()
    await state.clear()
    await callback.message.edit_text(
        'Выберите, что Вы хотите отредактировать:',
        reply_markup=keyboard,
    )


@dp.callback_query(F.data == 'blank')
async def edit_message(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.from_user.id != int(messages['owner_id']):
        return
    await callback.answer()
    messages[callback.data[6:]] = ''
    messages_str = json.dumps(messages, ensure_ascii=False, indent=4)
    async with aiofiles.open('messages.json', 'w') as file:
        await file.write(messages_str)
    answer = await callback.message.answer('Успешно изменено!')
    await return_back(callback, state)
    await asyncio.sleep(1)
    await answer.delete()


@dp.callback_query(F.data.startswith('edit_'))
async def edit_message(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.from_user.id != int(messages['owner_id']):
        return
    await callback.answer()
    await state.set_state(Edit.edit)
    await state.update_data(
        edit=callback.data[5:],
        callback=callback,
    )
    await callback.message.edit_text(
        'Введите новое сообщение:',
        reply_markup=editor_keyboard,
    )


@dp.message(Command('edit'))
@dp.message(CommandStart())
async def edit(message: Message) -> None:
    if not messages['owner_id']:
        messages['owner_id'] = message.from_user.id
        messages_str = json.dumps(messages, ensure_ascii=False, indent=4)
        async with aiofiles.open('messages.json', 'w') as file:
            await file.write(messages_str)
    if message.from_user.id != int(messages['owner_id']):
        return
    await message.answer(
        'Выберите, что Вы хотите отредактировать:',
        reply_markup=keyboard,
    )


async def main() -> None:
    asyncio.create_task(background())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
