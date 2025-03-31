import asyncio
from aiogram import Bot, Dispatcher
from app.handlers import router
from app.database.models import async_main
from app.handlers import send_message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

import app.database.requests as rq
import os


async def main():
    await async_main()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    users = await rq.get_all_users()
    for user_id in users:
        print(user_id)
        asyncio.create_task(send_message(user_id, FSMContext, bot))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот отключён")