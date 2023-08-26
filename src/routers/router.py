from aiogram import F, Router

from src.routers.admin.router import router as admin_router
from src.routers.consultant.router import router as consultant_router
from src.routers.user.router import router as user_router

router = Router()

router.include_router(admin_router)
router.include_router(consultant_router)
router.include_router(user_router)
router.message.filter(F.chat.type == "private")
