from aiogram import types


kb = [
    [
        types.KeyboardButton(text="Добавить автомобиль"),
        types.KeyboardButton(text="Редактировать автомобиль")
    ],
    [
        types.KeyboardButton(text="Редактировать профиль"),
        types.KeyboardButton(text="Заказы")
    ]
]

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
