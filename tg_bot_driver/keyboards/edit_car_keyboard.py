from aiogram import types


kb = [
    [types.InlineKeyboardButton(text="Редактировать регистрационный номер автомобиля", callback_data="edit_car_number")],
    [types.InlineKeyboardButton(text="Редактировать марку автомобиля", callback_data="edit_vendor")],
    [types.InlineKeyboardButton(text="Редактировать модель автомобиля", callback_data="edit_model")],
    [types.InlineKeyboardButton(text="Изменить тип кузов", callback_data="edit_load_capacity")],
    [types.InlineKeyboardButton(text="Изменить объем", callback_data="edit_volume")]
]

edit_car_keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
