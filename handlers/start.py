from dispatcher import dp, bot, cursor, connect
from configurator import config
import handlers.keyboard as kb
from aiogram import types


@dp.message_handler(commands=['start'], commands_prefix="/!", chat_type=types.ChatType.PRIVATE)
async def start_cmd(message: types.Message):
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id numeric,
                user_name varchar,
                username varchar
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
                    fullname varchar,
                    date_of_birth varchar,
                    phone_number numeric,
                    region varchar,
                    job varchar,
                    take_to_work varchar,
                    balance integer,
                    filial varchar
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS admins(
                    user_id numeric,
                    user_name varchar,
                    login varchar,
                    password varchar,
                    remember_me varchar,
                    status varchar
    )""")
    connect.commit()
    cursor.execute(f"SELECT * FROM users WHERE user_id='{message.from_user.id}'")
    users = cursor.fetchone()
    if not message.from_user.username:
        await bot.send_message(message.chat.id, f"Sizda foydalanuvchi nomi yo'q")
        return
    if users is None:
        cursor.execute(f"INSERT INTO users VALUES(?, ?, ?)", (f"{message.from_user.id}", f"{message.from_user.first_name}", f"{message.from_user.username}"))
        connect.commit()
        await bot.send_message(message.chat.id, f"Assalomu Aleykum {message.from_user.get_mention(as_html=True)}", reply_markup=kb.filiali_btn)
        await bot.send_message(config.bot.owner, f"Botga yangi foydalanuvchi kirdi\n"
                                                 f"{message.from_user.get_mention(as_html=True)}\n<")
    else:
        await bot.send_message(message.chat.id, f"Assalomu Aleykum {message.from_user.get_mention(as_html=True)}", reply_markup=kb.filiali_btn)
