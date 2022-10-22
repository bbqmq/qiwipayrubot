from aiogram.utils import executor
from pathes.qiwi import checker

if __name__ == "__main__":
    from pathes.admin import dp
    from pathes.client import dp
    dp.loop.create_task(checker.run())
    executor.start_polling(dp, skip_updates=True)