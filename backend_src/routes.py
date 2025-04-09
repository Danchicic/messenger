from modules import main_router
from auth.routes import router as auth_router

main_router.include_router(auth_router)
