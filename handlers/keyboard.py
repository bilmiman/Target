from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


filiali_btn = ReplyKeyboardMarkup(resize_keyboard=True)
tinchlik_btn = KeyboardButton(text='Tinchlik filial')
sergeli_btn = KeyboardButton(text='Sergeli filial')
filiali_btn.add(tinchlik_btn, sergeli_btn)


admin_btn = ReplyKeyboardMarkup(resize_keyboard=True)
xodim_btn = KeyboardButton(text='Xodim qoshish')
xodim_remove_btn = KeyboardButton(text='Xodimni olip tashlash')
jarima_btn = KeyboardButton(text='Jarima berish')
bonus_btn = KeyboardButton(text='Bonus berish')
balance_check = KeyboardButton(text='Balans tekshirish')
xodimlar = KeyboardButton(text='Xodimlar')
admin_btn.add(xodim_btn, xodim_remove_btn)
admin_btn.add(xodimlar, jarima_btn)
admin_btn.add(bonus_btn, balance_check)


cancel_btn = ReplyKeyboardMarkup(resize_keyboard=True)
cancel = KeyboardButton(text='Bekor qilish')
cancel_btn.add(cancel)


nazad_btn = ReplyKeyboardMarkup(resize_keyboard=True)
nazad = KeyboardButton(text='Orqaga')
nazad_btn.add(nazad)

def staff(db):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for user in db:
        btn.insert(KeyboardButton(text=f'{user[0]}'))
    btn.add(KeyboardButton('Orqaga'))
    return btn


def give(db):
    btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for user in db:
        btn.insert(KeyboardButton(text=f'{user[0]}'))
    btn.add(KeyboardButton('Orqaga'))
    return btn
