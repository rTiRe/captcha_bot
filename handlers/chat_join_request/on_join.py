from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import ChatJoinRequest, InlineKeyboardButton, Message, FSInputFile
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramForbiddenError
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import settings
from messages import get_message
from states import CaptchaStates

from .router import router


async def _decline_join_request(request: ChatJoinRequest, message: Message) -> None:
    await request.decline()
    timeout_message: Message = await get_message('timeout_messages', request)
    if timeout_message:
        await message.edit_reply_markup()
        if message.text:
            await message.edit_text(
                text=timeout_message.get('text'),
                business_connection_id=timeout_message.get('business_connection_id'),
                entities=timeout_message.get('entities', []),
                link_preview_options=timeout_message.get('link_preview_options'),
            )
        if message.caption:
            await message.edit_caption(
                business_connection_id=timeout_message.get('business_connection_id'),
                caption=timeout_message.get('text'),
                caption_entities=timeout_message.get('entities', []),
            )
    else:
        await message.delete()


async def _send_hello(request: ChatJoinRequest) -> None:
    hello_message = await get_message('hello_messages', request)
    if hello_message:
        await Message(**hello_message).as_(request.bot).send_copy(request.from_user.id)


async def _send_captcha(request: ChatJoinRequest, state: FSMContext) -> Message:
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
            await message.edit_reply_markup(reply_markup=keyboard.as_markup())
        await state.update_data(request=request)
    return message


@router.chat_join_request()
async def on_join(request: ChatJoinRequest, state: FSMContext, scheduler: AsyncIOScheduler) -> None:
    try:
        await _send_hello(request)
    except TelegramForbiddenError as exception:
        if not 'bot was blocked by the user' in exception.message:
            return exception
        await request.decline()
        return
    message = await _send_captcha(request, state)
    await state.set_state(CaptchaStates.waiting_captcha)
    print(datetime.now() + timedelta(seconds=settings.JOIN_REQUEST_TIMEOUT))
    scheduler.add_job(
        _decline_join_request,
        trigger='date',
        run_date=datetime.now() + timedelta(seconds=settings.JOIN_REQUEST_TIMEOUT),
        id=f'{message.chat.id}{message.message_id}',
        kwargs={
            'request': request,
            'message': message,
        },
    )
    if not scheduler.running: scheduler.start()
