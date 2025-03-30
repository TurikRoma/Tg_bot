import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main
from app.handlers import send_message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import app.database.requests as rq


async def main():
    await async_main()
    bot = Bot(token='7310959822:AAH7gEMRRZsDO7cYR8xFWb-YM-JJjftKxUc')
    users = await rq.get_all_users()
    for user_id in users:
        asyncio.create_task(send_message(user_id, FSMContext, bot))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот отключён")