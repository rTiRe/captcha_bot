import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import ChatJoinRequest, InlineKeyboardButton, Message
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder

from messages import get_message
from states import CaptchaStates

from .router import router


async def _send_hello(request: ChatJoinRequest) -> None:
    hello_message = await get_message('hello_messages', request)
    if hello_message:
        await Message(**hello_message).as_(request.bot).send_copy(request.from_user.id)


async def _send_captcha(request: ChatJoinRequest, state: FSMContext) -> None:
    captcha_message = await get_message('captcha_messages', request)
    captcha_button = await get_message('captcha_buttons', request)
    if captcha_message:
        message = await Message(**captcha_message).as_(request.bot).send_copy(request.from_user.id)
        if captcha_button:
            keyboard = InlineKeyboardBuilder()
            link = await create_start_link(
                request.bot,
                f'approve_{request.chat.id}_{message.chat.id}_{message.message_id}',
                encode=True,
            )
            keyboard.add(InlineKeyboardButton(
                text=captcha_button['text'],
                url=link,
            ))
            asyncio.create_task(message.edit_reply_markup(reply_markup=keyboard.as_markup()))
        await state.update_data(request=request)


@router.chat_join_request()
async def on_join(request: ChatJoinRequest, state: FSMContext) -> None:
    await _send_hello(request)
    await _send_captcha(request, state)
    await state.set_state(CaptchaStates.waiting_captcha)
