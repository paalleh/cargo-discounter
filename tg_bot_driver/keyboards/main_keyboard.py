from aiogram import types


kb = [
    [
        types.KeyboardButton(text="Добавить автомобиль"),
        types.KeyboardButton(text="Мой гараж")
    ],
    [
        types.KeyboardButton(text="Мой профиль"),
        types.KeyboardButton(text="Заказы")
    ]
]

main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
