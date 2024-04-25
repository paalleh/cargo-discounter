from aiogram import types


kb = [
    [
        types.KeyboardButton(text="Добавить автомобиль"),
        types.KeyboardButton(text="Мой профиль")
    ]
]

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
