from aiogram import types


def get_check_car_keyboard(cars_amount: int) -> types.InlineKeyboardMarkup:
    kb = []

    for i in range(cars_amount):
        kb.append(
            [types.InlineKeyboardButton(text=f"Редактировать автомобиль номер: {i}",
                                        callback_data=f"edit_my_car_{i}")]
        )
    return types.InlineKeyboardMarkup(inline_keyboard=kb)
