import logging
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from configurator import config, make_config

logging.basicConfig(level=logging.INFO)
if not make_config("config.ini"):
    logging.error("Errors while parsing config file. Exiting.")
    exit(1)

if not config.bot.token:
    logging.error("No token provided")
    exit(1)

bot = Bot(token=config.bot.token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())



connect = sqlite3.connect("db.db")
cursor = connect.cursor()


