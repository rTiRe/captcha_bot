from aiogram import Router

from .messages.router import router as messages_router

router = Router()
router.include_router(messages_router)
