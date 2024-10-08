from aiogram import Router

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from middlewares.scheduler_middleware import SchedulerMiddleware
from . import join_router, settings_router

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

router = Router()
join_router.chat_join_request.middleware(SchedulerMiddleware(scheduler))
router.include_router(join_router)
router.include_router(settings_router)
router.message.middleware(SchedulerMiddleware(scheduler))
