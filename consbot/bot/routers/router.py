from aiogram import F, Router

from consbot.bot.routers.admin.router import router as admin_router
from consbot.bot.routers.consultant.router import router as consultant_router
from consbot.bot.routers.user.router import router as user_router

router = Router()

router.include_router(admin_router)
router.include_router(consultant_router)
router.include_router(user_router)
router.message.filter(F.chat.type == "private")
