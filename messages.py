import asyncio

import emoji
from aiogram.fsm.context import FSMContext
from aiogram.types import ChatJoinRequest, Message
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.sqlite import insert

from database.database import get_db
from database.models.messages import (CaptchaButton, CaptchaMessage,
                                      HelloMessage, WelcomeMessage)
from database.models.users import Admin, User

messages_models: dict[str, HelloMessage | CaptchaButton | CaptchaMessage | WelcomeMessage] = {
    'captcha_buttons': CaptchaButton,
    'captcha_messages': CaptchaMessage,
    'hello_messages': HelloMessage,
    'welcome_messages': WelcomeMessage,
}
messages = {}
owner_id = 0

async def _fill_data() -> None:
    global owner_id
    global messages
    global messages_models
    async with get_db() as db:
        for key, value in messages_models.items():
            await asyncio.sleep(0)
            result = await db.execute(select(value).where(value.is_active == 1))
            data = result.fetchone()
            messages[key] = data[0].message if data else ''
        result = await db.execute(select(Admin).where(Admin.id == 1))
        data = result.fetchone()
        owner_id = data[0].user_id if data else 0


async def add_user(id: int) -> None:
    async with get_db() as db:
        statement = insert(User).values(
            user_id=id,
        ).on_conflict_do_nothing(
            index_elements=['user_id'],
        )
        await db.execute(statement)
        await db.commit()


async def set_owner_id(id: int) -> None:
    global owner_id
    owner = Admin(user_id=id)
    async with get_db() as db:
        db.add(owner)
        await db.commit()
    owner_id = id


async def get_owner_id() -> int:
    global owner_id
    return owner_id


async def add_admin_id(id: int) -> None:
    messages['admins_ids'].append(id)
    model = Admin(id=id)
    async with get_db() as db:
        db.add(model)
        await db.commit()


async def remove_admin_id(id: int) -> None:
    messages['admins_ids'].remove(id)
    async with get_db() as db:
        statement = delete(Admin).where(Admin.id == id)
        await db.execute(statement)
        await db.commit()


async def get_admins_ids() -> list[int]:
    return messages.get('admins_ids', [])


async def _set_active_message_to_inactive(
    message_model: HelloMessage | CaptchaButton | CaptchaMessage | WelcomeMessage
) -> None:
    async with get_db() as db:
        statement = update(message_model).where(message_model.is_active == 1).values(is_active=0)
        await db.execute(statement)
        await db.commit()


async def set_message(
    message_type: str,
    message: dict,
    added_by: int,
    is_active: bool = False,
) -> None:
    message_model = messages_models.get(message_type)
    if not message_model:
        return
    record = message_model(message=message, added_by=added_by, is_active=is_active)
    if is_active:
        await _set_active_message_to_inactive(message_model)
    async with get_db() as db:
        db.add(record)
        await db.commit()
    if is_active:
        messages[message_type] = message


async def _update_length_with_emojies(string: str, length: int) -> int:
    for object in emoji.emoji_list(string):
        length += object['match_end'] - object['match_start']
    return length


async def adjust_entities_multiple(
    text: str,
    entities: list[dict],
    placeholder: str,
    replacement: str,
) -> tuple[str, list[dict]]:
    placeholder_len = len(placeholder)
    replacement_len = len(replacement)
    replacement_len = await _update_length_with_emojies(replacement, replacement_len)
    diff = replacement_len - placeholder_len
    placeholder_start = text.find(placeholder)
    while placeholder_start != -1:
        await asyncio.sleep(0)
        text_before = text[:placeholder_start]
        text_after = text[placeholder_start+placeholder_len:]
        text = f'{text_before}{replacement}{text_after}'
        placeholder_end = placeholder_start + placeholder_len
        for entity in entities:
            await asyncio.sleep(0)
            entity_start = entity['offset']
            if entity_start >= placeholder_end:
                entity['offset'] += diff
            elif placeholder_start <= entity_start < placeholder_end:
                placeholder_start = await _update_length_with_emojies(text_before, placeholder_start)
                entity['offset'] = placeholder_start
                entity['length'] = replacement_len
            elif placeholder_start < (entity_start + entity['length']):
                entity['length'] += diff
        placeholder_start = text.find(placeholder)
    return text, entities


async def _get_channel_name(
    request: ChatJoinRequest = None,
    message: tuple[Message, int | str] = None,
) -> str | None:
    if request:
        return request.chat.full_name
    if message:
        return (await message[0].bot.get_chat(message[1])).full_name


async def replace_placeholders(
    message: dict,
    data: ChatJoinRequest | FSMContext,
) -> dict:
    if isinstance(data, FSMContext):
        datas = await data.get_data()
        data = datas['message']
        channel_id = datas['channel_id']
    placeholders = {
        r'{user_full_name}': data.from_user.full_name,
        r'{user_first_name}': data.from_user.first_name,
        r'{user_last_name}': str(data.from_user.last_name or ''),
    }
    channel_name = ''
    if isinstance(data, ChatJoinRequest):
        channel_name = await _get_channel_name(request=data)
    else:
        channel_name = await _get_channel_name(message=(data, channel_id))
    if channel_name:
        placeholders[r'{channel_name}'] = channel_name
    for placeholder, replacement in placeholders.items():
        await asyncio.sleep(0)
        result = await adjust_entities_multiple(
            message.get('text', message.get('caption', '')),
            message.get('entities', message.get('caption_entities', [])),
            placeholder,
            replacement,
        )
        if message.get('text'):
            message['text'], message['entities'] = result
        else:
            message['caption'], message['caption_entities'] = result
    return message


async def get_message(message_name: str, data: FSMContext | ChatJoinRequest) -> dict:
    message: dict = messages[message_name]
    if message:
        return await replace_placeholders(message.copy(), data)
    return message
