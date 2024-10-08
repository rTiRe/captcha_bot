from aiogram import Router

from . import join_router, settings_router

router = Router()
router.include_router(join_router)
router.include_router(settings_router)
