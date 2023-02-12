from aiogram.dispatcher import FSMContext

from dispatcher import dp, bot, cursor, connect
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State

class add_admin(StatesGroup):
    admin_id = State()
    name = State()
    login = State()
    password = State()

def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False
@dp.message_handler(commands=['add_admin'], chat_type=types.ChatType.PRIVATE, commands_prefix="/!")
async def owner_cmd(message: types.Message):
    if message.text.split()[1] == 'target.uz':
        cursor.execute(f"INSERT INTO admins VALUES(?, ?, ?, ?, ?, ?)", (0, 0, 0, 0, 'no', 'user'))
        connect.commit()
        await bot.send_message(message.chat.id, f'Admini id raqamini tashlang')
        await add_admin.admin_id.set()
    else:
        return


@dp.message_handler(state=add_admin.admin_id, chat_type=types.ChatType.PRIVATE)
async def owner_cmd(message: types.Message):
    number = is_number(message.text)
    if number == True:
        cursor.execute(f'UPDATE admins SET user_id="{int(message.text)}" WHERE user_id="0"')
        connect.commit()
        await bot.send_message(message.chat.id, f"Admini Ismini yozing")
        await add_admin.name.set()
    else:
        await bot.send_message(message.chat.id, f'Admini id raqamini tashlang')
        await add_admin.admin_id.set()


@dp.message_handler(state=add_admin.name, chat_type=types.ChatType.PRIVATE)
async def owner_cmd(message: types.Message):
    cursor.execute(f'UPDATE admins SET user_name="{message.text}" WHERE user_name="0"')
    connect.commit()
    await bot.send_message(message.chat.id, f"Adminga login oylap toping")
    await add_admin.login.set()


@dp.message_handler(state=add_admin.login, chat_type=types.ChatType.PRIVATE)
async def owner_cmd(message: types.Message):
    cursor.execute(f'UPDATE admins SET login="{message.text}" WHERE login="0"')
    connect.commit()
    await bot.send_message(message.chat.id, f"Adminga parol oylap toping")
    await add_admin.password.set()

@dp.message_handler(state=add_admin.password, chat_type=types.ChatType.PRIVATE)
async def owner_cmd(message: types.Message, state: FSMContext):
    cursor.execute(f'UPDATE admins SET password="{message.text}" WHERE password="0"')
    cursor.execute(f'UPDATE admins SET remember_me="no" WHERE remember_me="0"')
    cursor.execute(f'UPDATE admins SET status="admin" WHERE password="{message.text}"')
    connect.commit()
    await bot.send_message(message.chat.id, f"Admin muvaffaqiyatli qoshildi")
    await state.finish()


class rv_admin(StatesGroup):
    admin_id = State()
@dp.message_handler(commands=['rv_admin'], chat_type=types.ChatType.PRIVATE, commands_prefix="/!")
async def owner_cmd(message: types.Message):
    if message.text.split()[1] == 'target.uz':
        await bot.send_message(message.chat.id, f'Admini id raqamini tashlang')
        await rv_admin.admin_id.set()
    else:
        return


@dp.message_handler(state=rv_admin.admin_id, chat_type=types.ChatType.PRIVATE)
async def owner_cmd(message: types.Message):
    number = is_number(message.text)
    if number == True:
        cursor.execute(f"UPDATE admins SET user_id='{int(message.text)}' WHERE user_id='0'")
        connect.commit()
        await bot.send_message(message.chat.id, f"Admin muvaffaqiyatli ochirildi")
    else:
        await bot.send_message(message.chat.id, f'Admini id raqamini tashlang')
        await rv_admin.admin_id.set()
