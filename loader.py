from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import data.database as db
import data.config as config
from pathes.qiwi import qiwi as qiwi

#other
cfg = config.Cfg()
loop = asyncio.get_event_loop()
bot = Bot(token=cfg.token)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)