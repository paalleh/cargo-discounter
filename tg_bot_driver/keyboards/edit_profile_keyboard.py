from aiogram import types


kb = [
    [types.InlineKeyboardButton(text="Редактировать имя", callback_data="edit_first_name")],
    [types.InlineKeyboardButton(text="Редактировать фамилию", callback_data="edit_last_name")],
    [types.InlineKeyboardButton(text="Редактировать телефон", callback_data="edit_phone")],
    [types.InlineKeyboardButton(text="Изменить геолокацию", callback_data="edit_location")],
    [types.InlineKeyboardButton(text="Редактировать водительские права", callback_data="edit_driver_license")]
]

edit_profile_keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)