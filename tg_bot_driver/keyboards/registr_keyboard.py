from aiogram import types


kb = [
    [types.KeyboardButton(text="Зарегистрироваться")]
]

registr_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)