from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from utils.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage=RedisStorage2()
dp = Dispatcher(bot, storage=storage) 