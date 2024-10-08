from typing import Any, Callable, Awaitable, Self

from aiogram import BaseMiddleware
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class SchedulerMiddleware(BaseMiddleware):
    __flyweight : dict[AsyncIOScheduler, Self] = {}

    def __new__(cls, scheduler: AsyncIOScheduler) -> None:
        if scheduler not in cls.__flyweight.keys():
            instance = super().__new__(cls)
            cls.__flyweight[scheduler] = instance
        return cls.__flyweight[scheduler]

    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data['scheduler'] = self.scheduler
        return await handler(event, data)

