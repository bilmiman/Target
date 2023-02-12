from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dispatcher import connect, cursor, dp, bot
from aiogram import types
import handlers.state_FSM as fsm
import handlers.keyboard as kb

remove = []

@dp.message_handler(Text('Xodimni olip tashlash', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def remove_employee_cmd(message: types.Message):
    cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
    users = cursor.fetchone()
    cursor.execute(f"SELECT * FROM employees")
    count = cursor.fetchall()
    cursor.execute(f"SELECT * FROM employees")
    count_users = cursor.fetchmany(len(count))
    if not count_users:
        await bot.send_message(message.chat.id, f'Xodimlar xali kiritilmagan')
        return
    if users[5] == 'admin':
        filial_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tinchlik_filial = types.KeyboardButton(text='Tinchlik filial')
        sergeli_filial = types.KeyboardButton(text='Sergeli filial')
        filial_btn.add(tinchlik_filial, sergeli_filial)
        filial_btn.add(kb.nazad)
        await bot.send_message(message.chat.id, f'Qaysi filial?', reply_markup=filial_btn)
        await fsm.remove_employee.remove_employee.set()
    else:
        return

@dp.message_handler(state=fsm.remove_employee.remove_employee, chat_type=types.ChatType.PRIVATE)
async def remove_employee_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        remove.append(message.text)
        cursor.execute(f"SELECT * FROM employees")
        count = cursor.fetchall()
        cursor.execute(f"SELECT * FROM employees")
        count_users = cursor.fetchmany(len(count))
        remove.append(message.text)
        await bot.send_message(message.chat.id, f'Qaysi xodimni olib tashlamoqchisiz?', reply_markup=kb.give(count_users))
        await fsm.remove_employee.filial.set()
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)

@dp.message_handler(state=fsm.remove_employee.filial, chat_type=types.ChatType.PRIVATE)
async def remove_employee_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'DELETE FROM employees WHERE fullname="{message.text}" AND filial="{remove[0]}"')
        connect.commit()
        remove.clear()
        await bot.send_message(message.chat.id, f'Xodim muvaffaqiyatli olib tashaldi', reply_markup=kb.admin_btn)
        await state.finish()
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


