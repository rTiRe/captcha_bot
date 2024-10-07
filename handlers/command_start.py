from .router import router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from .chat_join_request.captcha_approve import approve
from aiogram.fsm.context import FSMContext


@router.message(CommandStart(deep_link=True, deep_link_encoded=True))
async def start_encoded(message: Message, command: CommandObject, state: FSMContext) -> None:
    if command.args.startswith('approve_'):
        await approve(message, command, state)