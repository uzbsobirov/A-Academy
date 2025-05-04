from aiogram import Router

from filters import ChatPrivateFilter


def setup_routers() -> Router:
    from .users import admin, start, help, answers, backs, channels_require, admins_list, test_settings, do_test
    from .errors import error_handler

    router = Router()

    # Agar kerak bo'lsa, o'z filteringizni o'rnating
    start.router.message.filter(ChatPrivateFilter(chat_type=["private"]))

    router.include_routers(do_test.router, admin.router, start.router, help.router, error_handler.router, answers.router,
                           backs.router, channels_require.router, admins_list.router, test_settings.router,
                           )

    return router
