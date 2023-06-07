from loguru import logger

from app import misc
from app.bot.handlers import admin_router, main_router
from db.init_db import init_db
from utils.logger import configure_logger


def setup():
    import app.bot.middlewares.big_bro  # noqa
    misc.dp.include_router(main_router)


async def on_startup():
    configure_logger(True)

    try:
        await init_db()
    except ConnectionRefusedError:
        logger.error("Failed to connect to database ")
        exit(1)

    setup()
    logger.info("Success init")


async def on_shutdown():
    logger.info("Success exit")


if __name__ == '__main__':
    misc.dp.startup.register(on_startup)
    misc.dp.shutdown.register(on_shutdown)
    misc.dp.run_polling(misc.bot)
