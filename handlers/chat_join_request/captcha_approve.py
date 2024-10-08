import asyncio
from datetime import datetime

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from messages import add_user, get_message


async def approve(message: Message, command: CommandObject, state: FSMContext) -> None:
    await message.delete()
    args = command.args.split('_')
    try:
        asyncio.create_task(message.bot.approve_chat_join_request(
            args[1],
            message.from_user.id,
        ))
    except TelegramBadRequest:
        return
    asyncio.create_task(message.bot.delete_message(int(args[2]), int(args[3])))
    await state.update_data(message=message, channel_id=args[1])
    asyncio.create_task(add_user(message.from_user.id))
    welcome_message = await get_message('welcome_messages', state)
    await message.answer('now')
    if welcome_message:
        await Message(**welcome_message).as_(message.bot).send_copy(message.chat.id)
