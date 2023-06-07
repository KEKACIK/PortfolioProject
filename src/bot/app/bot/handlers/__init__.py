from aiogram import Router

from .admin import admin_router
from .settings import settings_router
from .start import start_router

main_router = Router()
main_router.include_router(start_router)
main_router.include_router(admin_router)
main_router.include_router(settings_router)
