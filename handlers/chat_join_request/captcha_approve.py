from aiogram.filters import CommandObject
from aiogram.types import Message
from aiogram.utils.serialization import deserialize_telegram_object_to_python
from aiogram.exceptions import TelegramBadRequest
from messages import get_message, add_user
from aiogram.fsm.context import FSMContext


async def approve(message: Message, command: CommandObject, state: FSMContext) -> None:
    await message.delete()
    args = command.args.split('_')
    try:
        await message.bot.approve_chat_join_request(
            args[1],
            message.from_user.id,
        )
    except TelegramBadRequest:
        return
    await message.bot.delete_message(int(args[2]), int(args[3]))
    await state.update_data(message=message, channel_id=args[1])
    await add_user(message.from_user.id)
    welcome_message = await get_message('welcome_messages', state)
    if welcome_message:
        await Message(**welcome_message).as_(message.bot).send_copy(message.chat.id)
