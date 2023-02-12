try:
    from loader import executor, dp, logger
    import asyncio

    import handlers
    from utils.set_bot_commands import setup_bot_commands
    from database.models import db_init
    from parsing.search_all import search_all

    if __name__ == '__main__':
        db_init()
        loop = asyncio.get_event_loop()
        loop.create_task(search_all())
        executor.start_polling(dp, skip_updates=True, on_startup=setup_bot_commands, )
except Exception as e:
    logger.info(e)
