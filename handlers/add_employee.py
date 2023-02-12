from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dispatcher import connect, cursor, dp, bot
from aiogram import types
import handlers.state_FSM as fsm
import handlers.keyboard as kb



@dp.message_handler(Text('Bekor qilish', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def add_employee_cmd(message: types.Message, state: FSMContext):
    try:
        cursor.execute(f'SELECT * FROM employees WHERE filial="0"')
        employeess = cursor.fetchone()
        if employeess is None:
            await state.finish()
            await bot.send_message(message.chat.id, f'Bekor qilindi', reply_markup=kb.admin_btn)
        else:
            cursor.execute(f'DELETE FROM employees WHERE filial="0"')
            connect.commit()
            await state.finish()
            await bot.send_message(message.chat.id, f'Bekor qilindi', reply_markup=kb.admin_btn)
    except:
        return



@dp.message_handler(Text('Xodim qoshish', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def add_employee_cmd(message: types.Message):
    cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
    users = cursor.fetchone()
    if users[5] == 'admin':
        cursor.execute(f"INSERT INTO employees VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (f"0", f"0", f"0", f"0", f"0", f"0", f"0", f"0"))
        connect.commit()
        await bot.send_message(message.chat.id, f'Xodimni Familiyasini, Ismi, Otasining ismi yozing', reply_markup=kb.cancel_btn)
        await fsm.add_employee.add_fullname.set()
    else:
        return


def probel(text):
    n = text.split(".")
    if text.endswith("."):
        n = text.split(".")[:-1]
    for i in range(1, len(n)):
        return n[i].count(' ')


@dp.message_handler(state=fsm.add_employee.add_fullname, content_types=types.ContentType.TEXT)
async def add_user_name_cmd(message: types.Message, state: FSMContext):
    pr = probel(f".{message.text}.")
    if message.text != 'Bekor qilish':
        if pr >= 2:
            cursor.execute(f'UPDATE employees SET fullname="{message.text}" WHERE fullname="0"')
            connect.commit()
            await bot.send_message(message.chat.id, f'Xodimni tug\'ulgan sanasini yozing\nMisol: 15.02.1985', reply_markup=kb.cancel_btn)
            await fsm.add_employee.add_date_of_birth.set()
        else:
            await bot.send_message(message.chat.id, f"Xodimni Familiyasini, Ismi, Otasining ismi yozing", reply_markup=kb.cancel_btn)
            await fsm.add_employee.add_fullname.set()
    else:
        await state.finish()
        cursor.execute(f'DELETE FROM employees WHERE filial="0"')
        connect.commit()
        await bot.send_message(message.chat.id, f'Bekor qilindi', reply_markup=kb.admin_btn)


@dp.message_handler(state=fsm.add_employee.add_date_of_birth, content_types=types.ContentType.TEXT)
async def add_user_name_cmd(message: types.Message):
    cursor.execute(f'UPDATE employees SET date_of_birth="{message.text}" WHERE date_of_birth="0"')
    connect.commit()
    await bot.send_message(message.chat.id, f'Xodimni telefon raqamini yozing\nMisol: +998991234567', reply_markup=kb.cancel_btn)
    await fsm.add_employee.add_phone_number.set()


@dp.message_handler(state=fsm.add_employee.add_phone_number, content_types=types.ContentType.TEXT)
async def add_user_name_cmd(message: types.Message):
    cursor.execute(f'UPDATE employees SET phone_number="{message.text}" WHERE phone_number="0"')
    connect.commit()
    await bot.send_message(message.chat.id, f'Xodimni viloyat/shahar yozing', reply_markup=kb.cancel_btn)
    await fsm.add_employee.add_region.set()


@dp.message_handler(state=fsm.add_employee.add_region, content_types=types.ContentType.TEXT)
async def add_user_name_cmd(message: types.Message):
    cursor.execute(f'UPDATE employees SET region="{message.text}" WHERE region="0"')
    connect.commit()
    await bot.send_message(message.chat.id, f'Xodimni lavozimini yozing', reply_markup=kb.cancel_btn)
    await fsm.add_employee.add_job.set()

@dp.message_handler(state=fsm.add_employee.add_job, content_types=types.ContentType.TEXT)
async def add_user_name_cmd(message: types.Message):
    cursor.execute(f'UPDATE employees SET job="{message.text}" WHERE job="0"')
    connect.commit()
    await bot.send_message(message.chat.id, f'Xodimni ishga olingan kun yozing\nMisol: 15.02.2022', reply_markup=kb.cancel_btn)
    await fsm.add_employee.add_take_to_work.set()

@dp.message_handler(state=fsm.add_employee.add_take_to_work, content_types=types.ContentType.TEXT)
async def add_user_name_cmd(message: types.Message):
    cursor.execute(f'UPDATE employees SET take_to_work="{message.text}" WHERE take_to_work="0"')
    connect.commit()
    filial_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
    tinchlik_filial = types.KeyboardButton(text='Tinchlik filial')
    sergeli_filial = types.KeyboardButton(text='Sergeli filial')
    cancel_btn = types.KeyboardButton(text='Bekor qilish')
    filial_btn.add(tinchlik_filial, sergeli_filial)
    filial_btn.add(cancel_btn)
    await bot.send_message(message.chat.id, f'Xodim qaysi filialda ishlaydi?', reply_markup=filial_btn)
    await fsm.add_employee.add_filial.set()


@dp.message_handler(state=fsm.add_employee.add_filial, content_types=types.ContentType.TEXT)
async def add_user_name_cmd(message: types.Message, state: FSMContext):
    cursor.execute(f'UPDATE employees SET filial="{message.text}" WHERE filial="0"')
    connect.commit()
    await bot.send_message(message.chat.id, f'Xodim muvaffaqiyatli kirdi', reply_markup=kb.admin_btn)
    await state.finish()
