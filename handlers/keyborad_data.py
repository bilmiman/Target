from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dispatcher import dp, bot, cursor, connect
from aiogram import types
import handlers.keyboard as kb
import handlers.state_FSM as fsm


def is_number(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


@dp.message_handler(Text('Orqaga', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def tinchlik_filiali_cmd(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, f'Bosh Menu', reply_markup=kb.filiali_btn)


@dp.message_handler(Text('Tinchlik filial', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def tinchlik_filiali_cmd(message: types.Message):
    cursor.execute(f'SELECT * FROM users WHERE user_id="{message.from_user.id}"')
    users = cursor.fetchone()
    cursor.execute(f'SELECT * FROM employees WHERE filial="Tinchlik filial"')
    count = cursor.fetchall()
    cursor.execute(f'SELECT * FROM employees WHERE filial="Tinchlik filial"')
    count_users = cursor.fetchmany(len(count))
    if not count_users:
        await bot.send_message(message.chat.id, f'Xodimlar xali kiritilmagan')
        return
    if users is None:
        await bot.send_message(message.chat.id, f"/start -ni bosing")
        return
    await bot.send_message(message.chat.id, f"Xodimlar ismi: ", reply_markup=kb.staff(count_users))
    await fsm.answers.start.set()


@dp.message_handler(Text('Sergeli filial', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def sergeli_filiali_cmd(message: types.Message):
    cursor.execute(f'SELECT * FROM users WHERE user_id="{message.from_user.id}"')
    users = cursor.fetchone()
    cursor.execute(f'SELECT * FROM employees WHERE filial="Sergeli filial"')
    count = cursor.fetchall()
    cursor.execute(f'SELECT * FROM employees WHERE filial="Sergeli filial"')
    count_users = cursor.fetchmany(len(count))
    if not count_users:
        await bot.send_message(message.chat.id, f'Xodimlar xali kiritilmagan')
        return
    if users is None:
        await bot.send_message(message.chat.id, f"/start -ni bosing")
        return
    await bot.send_message(message.chat.id, f"Xodimlar ismi: ", reply_markup=kb.staff(count_users))
    await fsm.answers.start.set()



@dp.message_handler(Text('Jarima berish', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def balans_berish_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        filial_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tinchlik_filial = types.KeyboardButton(text='Tinchlik filial')
        sergeli_filial = types.KeyboardButton(text='Sergeli filial')
        filial_btn.add(tinchlik_filial, sergeli_filial)
        filial_btn.add(kb.nazad)
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Qaysi filialdagi xodimga bermoqchisiz?', reply_markup=filial_btn)
            await fsm.give.filial_penalize.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(Text('Bonus berish', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def bonus_berish_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        filial_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tinchlik_filial = types.KeyboardButton(text='Tinchlik filial')
        sergeli_filial = types.KeyboardButton(text='Sergeli filial')
        filial_btn.add(tinchlik_filial, sergeli_filial)
        filial_btn.add(kb.nazad)
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Qaysi filialdagi xodimga bermoqchisiz?', reply_markup=filial_btn)
            await fsm.give.filial_bonus.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(Text('Balans tekshirish', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def balance_check_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        filial_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tinchlik_filial = types.KeyboardButton(text='Tinchlik filial')
        sergeli_filial = types.KeyboardButton(text='Sergeli filial')
        filial_btn.add(tinchlik_filial, sergeli_filial)
        filial_btn.add(kb.nazad)
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Qaysi filialdagi xodimni tekshirmoqchisiz?', reply_markup=filial_btn)
            await fsm.give.filial_balance_check.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)

@dp.message_handler(Text('Xodimlar', ignore_case=True), chat_type=types.ChatType.PRIVATE)
async def balance_check_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        filial_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        tinchlik_filial = types.KeyboardButton(text='Tinchlik filial')
        sergeli_filial = types.KeyboardButton(text='Sergeli filial')
        filial_btn.add(tinchlik_filial, sergeli_filial)
        filial_btn.add(kb.nazad)
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Qaysi filial?', reply_markup=filial_btn)
            await fsm.list.list.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)



@dp.message_handler(state=fsm.list.list)
async def who_penalize_state(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count = cursor.fetchall()
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count_users = cursor.fetchmany(len(count))
        if not count_users:
            await bot.send_message(message.chat.id, f'Xodimlar xali kiritilmagan')
            return
        userss = []
        num = 0
        for user in count_users:
            num += 1
            userss.append(f'{num} | {user[0]}')
        list = "\n".join(userss)
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Xodimlar:\n\n{list}', reply_markup=kb.admin_btn)
            await state.finish()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


give_penalize1 = []

@dp.message_handler(state=fsm.give.who_penalize)
async def who_penalize_state(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE fullname="{message.text}"')
        employees = cursor.fetchone()
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if employees is None:
            await bot.send_message(message.chat.id, f'Unday xodim yo\'q')
            return
        name = f"{employees[0]}"
        if users[5] == 'admin':
            give_penalize1.append(message.text)
            await bot.send_message(message.chat.id, f"Ism: {name.split(' ')[1]}\nFamilya: {name.split(' ')[0]}\nBalans: {employees[6]}\nFilial: {employees[7]}")
            await bot.send_message(message.chat.id, f"Qancha jarima bermoqchisiz?", reply_markup=types.ReplyKeyboardRemove())
            await fsm.give.give_penalize.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(state=fsm.give.give_penalize)
async def give_penalize_state(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE fullname="{give_penalize1[0]}"')
        employees = cursor.fetchone()
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if users[5] == 'admin':
            number = is_number(message.text)
            if number == True:
                cursor.execute(f'UPDATE employees SET balance="{employees[6] - int(message.text)}" WHERE fullname="{give_penalize1[0]}"')
                connect.commit()
                give_penalize1.clear()
                await bot.send_message(message.chat.id, f'Jarima muvaffaqiyatli berildi', reply_markup=kb.admin_btn)
                await state.finish()
            else:
                await bot.send_message(message.chat.id, f'Jarima faqat sonlar bilan bersa boladi')
                await fsm.give.give_penalize.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)



@dp.message_handler(state=fsm.give.who_balance_check)
async def who_penalize_state(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE fullname="{message.text}"')
        employees = cursor.fetchone()
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if employees is None:
            await bot.send_message(message.chat.id, f'Unday xodim yo\'q')
            return
        name = f"{employees[0]}"
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f"Ism: {name.split(' ')[1]}\nFamilya: {name.split(' ')[0]}\nBalans: {employees[6]}\nFilial: {employees[7]}", reply_markup=kb.admin_btn)
            await state.finish()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)

give_bonus1 = []

@dp.message_handler(state=fsm.give.who_bonus)
async def who_penalize_state(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE fullname="{message.text}"')
        employees = cursor.fetchone()
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if employees is None:
            await bot.send_message(message.chat.id, f'Unday xodim yo\'q')
            return
        name = f"{employees[0]}"
        if users[5] == 'admin':
            give_bonus1.append(message.text)
            await bot.send_message(message.chat.id, f"Ism: {name.split(' ')[1]}\nFamilya: {name.split(' ')[0]}\nBalans: {employees[6]}\nFilial: {employees[7]}")
            await bot.send_message(message.chat.id, f"Qancha bonus bermoqchisiz?")
            await fsm.give.give_bonus.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(state=fsm.give.give_bonus)
async def give_penalize_state(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE fullname="{give_bonus1[0]}"')
        employees = cursor.fetchone()
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if employees is None:
            await bot.send_message(message.chat.id, f'Unday xodim yo\'q')
            return
        if users[5] == 'admin':
            number = is_number(message.text)
            if number == True:
                cursor.execute(f'UPDATE employees SET balance="{employees[6] + int(message.text)}" WHERE fullname="{give_bonus1[0]}"')
                connect.commit()
                give_bonus1.clear()
                await bot.send_message(message.chat.id, f'Bonus muvaffaqiyatli berildi', reply_markup=kb.admin_btn)
                await state.finish()
            else:
                await bot.send_message(message.chat.id, f'Bonus faqat sonlar bilan bersa boladi')
                await fsm.give.give_bonus.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(state=fsm.give.filial_penalize)
async def balans_berish_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count = cursor.fetchall()
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count_users = cursor.fetchmany(len(count))
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if not count_users:
            await bot.send_message(message.chat.id, f'Xodimlar xali kiritilmagan')
            return
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Kimga jarima bermoqchisiz?', reply_markup=kb.give(count_users))
            await fsm.give.who_penalize.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(state=fsm.give.filial_bonus)
async def balans_berish_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count = cursor.fetchall()
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count_users = cursor.fetchmany(len(count))
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if not count_users:
            await bot.send_message(message.chat.id, f'Xodimlar xali kiritilmagan')
            return
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Kimga bonus bermoqchisiz?', reply_markup=kb.give(count_users))
            await fsm.give.who_bonus.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(state=fsm.give.filial_balance_check)
async def balans_berish_cmd(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count = cursor.fetchall()
        cursor.execute(f'SELECT * FROM employees WHERE filial="{message.text}"')
        count_users = cursor.fetchmany(len(count))
        cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if not count_users:
            await bot.send_message(message.chat.id, f'Xodimlar xali kiritilmagan')
            return
        if users[5] == 'admin':
            await bot.send_message(message.chat.id, f'Kimni balansini tekshirmoqchisiz?', reply_markup=kb.give(count_users))
            await fsm.give.who_balance_check.set()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)


@dp.message_handler(state=fsm.answers.start)
async def answer_date(message: types.Message, state: FSMContext):
    if message.text != 'Orqaga':
        cursor.execute(f'SELECT * FROM employees WHERE fullname="{message.text}"')
        employees = cursor.fetchone()
        cursor.execute(f'SELECT * FROM users WHERE user_id="{message.from_user.id}"')
        users = cursor.fetchone()
        if users is None:
            await bot.send_message(message.chat.id, f"/start -ni bosing")
            return
        if employees is None:
            return
        name = f"{employees[0]}"
        if message.text == employees[0]:
            await bot.send_message(message.chat.id, f"Ism: {name.split(' ')[1]}\nFamilya: {name.split(' ')[0]}\nBalans: {employees[6]}\nFilial: {employees[7]}", reply_markup=kb.filiali_btn)
            await state.finish()
        else:
            return
    else:
        await state.finish()
        await bot.send_message(message.chat.id, f'f"Assalomu Aleykum {message.from_user.get_mention(as_html=True)}', reply_markup=kb.filiali_btn)


