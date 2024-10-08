import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from messages import add_user, get_message


async def approve(message: Message, command: CommandObject, state: FSMContext, scheduler: AsyncIOScheduler) -> None:
    await message.delete()
    args = command.args.split('_')
    try:
        await message.bot.approve_chat_join_request(
            args[1],
            message.from_user.id,
        )
    except TelegramBadRequest:
        return
    scheduler.remove_job(f'{args[2]}{args[3]}')
    asyncio.create_task(message.bot.delete_message(int(args[2]), int(args[3])))
    await state.update_data(message=message, channel_id=args[1])
    asyncio.create_task(add_user(message.from_user.id))
    welcome_message = await get_message('welcome_messages', state)
    if welcome_message:
        await Message(**welcome_message).as_(message.bot).send_copy(message.chat.id)
