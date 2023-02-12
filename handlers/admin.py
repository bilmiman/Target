from aiogram.dispatcher import FSMContext
from dispatcher import dp, bot, cursor, connect
from aiogram import types
import handlers.keyboard as kb
import handlers.state_FSM as fsm


@dp.message_handler(commands=['admins'], commands_prefix="/!", chat_type=types.ChatType.PRIVATE)
async def admins_cmd(message: types.Message):
    cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
    admins = cursor.fetchone()
    if admins is None:
        await bot.send_message(message.chat.id, f'Siz administrator paneliga kira olmaysiz')
        return
    if admins[4] == 'yes':
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)
    else:
        await bot.send_message(message.chat.id, f'Loginingizni yozing', reply_markup=types.ReplyKeyboardRemove())
        await fsm.Admins.login.set()


@dp.message_handler(state=fsm.Admins.login, content_types=types.ContentType.TEXT)
async def login_cmd(message: types.Message):
    cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
    admins = cursor.fetchone()
    if message.text == admins[2]:
        await bot.send_message(message.chat.id, f'Parolingizni yozing')
        await fsm.Admins.password.set()
    else:
        await bot.send_message(message.chat.id, f'Login notog\'ri')
        await fsm.Admins.login.set()


@dp.message_handler(state=fsm.Admins.password, content_types=types.ContentType.TEXT)
async def password_cmd(message: types.Message):
    cursor.execute(f'SELECT * FROM admins WHERE user_id="{message.from_user.id}"')
    admins = cursor.fetchone()
    if message.text == admins[3]:
        remember_me_btn = types.ReplyKeyboardMarkup(resize_keyboard=True)
        remember_me_yes = types.KeyboardButton(text='✅ Ha')
        remember_me_no = types.KeyboardButton(text='❌ Yo\'q')
        remember_me_btn.add(remember_me_yes, remember_me_no)
        await bot.send_message(message.chat.id, f'Meni eslab qolish', reply_markup=remember_me_btn)
        await fsm.Admins.remember_me.set()
    else:
        await bot.send_message(message.chat.id, f'Parol notog\'ri')
        await fsm.Admins.password.set()


@dp.message_handler(state=fsm.Admins.remember_me, content_types=types.ContentType.TEXT)
async def remember_me_cmd(message: types.Message, state: FSMContext):
    if message.text == '✅ Ha':
        cursor.execute(f'UPDATE admins SET remember_me="yes" WHERE user_id="{message.from_user.id}"')
        connect.commit()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)
        await state.finish()
    elif message.text == "❌ Yo\'q":
        cursor.execute(f'UPDATE admins SET remember_me="no" WHERE user_id="{message.from_user.id}"')
        connect.commit()
        await bot.send_message(message.chat.id, f'Admin Hush Kelibsiz', reply_markup=kb.admin_btn)
        await state.finish()
