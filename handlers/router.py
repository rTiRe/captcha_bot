from aiogram import Router
from . import join_router
from . import settings_router

router = Router()
router.include_router(join_router)
router.include_router(settings_router)
