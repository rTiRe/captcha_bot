from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .chat_join_request.captcha_approve import approve
from .router import router


@router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_encoded(message: Message, command: CommandObject, state: FSMContext) -> None:
    if command.args.startswith('approve_'):
        await approve(message, command, state)