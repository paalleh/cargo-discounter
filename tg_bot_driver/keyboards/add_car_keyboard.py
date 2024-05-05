from aiogram import types


kb = [
    [types.KeyboardButton(text="Добавить автомобиль")]
]

add_car_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)