import logging
import json
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
# from aiogram.types import ParseMode
import requests

if os.path.exists('../.env'):
    load_dotenv('../.env')

print(os.getenv("CUSTOMER_BOT_TOKEN"))
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv("CUSTOMER_BOT_TOKEN"))
# print(bot)
# bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Функция для отправки сообщений
async def send_message(message, chat_id):
    await bot.send_message(chat_id, message, parse_mode=ParseMode.HTML)


# Функция для выполнения запроса GET к серверу
async def check_customer(customer_id):
    response = requests.get(f'http://64.23.210.118:8000/api/v1/customer/?customer_id={customer_id}')
    return response


# Функция для отправки данных на сервер запросом POST
async def send_customer(customer_id, first_name, last_name, phone):
    data = {
        'id': customer_id,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'is_blocked': 'false'
    }
    print(f"{first_name}Дело сделано")
    d = json.dumps(data)
    print(d)
    response = requests.post('http://64.23.210.118:8000/api/v1/customer/?', data=d)
    print(response)
    return response


# Функция для обработки команды /start

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    customer_id = message.from_user.id
    response = await check_customer(customer_id)
    if response.status_code == 400:
        await send_message(
            f"""{customer_id} Для возможности создания заказов необходимо зарегистрироваться. 
            Для регистрации нажмите кнопку 'Отправить номер'.""",
            message.chat.id)
        # Создаем клавиатуру с кнопкой "Отправить номер"
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button = KeyboardButton("Отправить номер", request_contact=True)
        keyboard.add(button)
        await message.answer("Для регистрации нажмите кнопку 'Отправить номер'.", reply_markup=keyboard)
    else:
        # Проверка на бан.
        customer_id = response.json()
        if customer_id["is_blocked"]:
            await message.answer("Вы заблокированы.")
        else:
            await message.answer("Вы можете приступить к работе.")


# Функция для обработки нажатия кнопки "Отправить номер"
# @dp.message_handler(lambda message: message.text == 'Отправить номер')
# async def send_phone_number(message: types.Message):
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def contacts(message: types.Message):
    await message.answer(f"Ваш номер: {message.contact.phone_number}", reply_markup=types.ReplyKeyboardRemove())
    response = await send_customer(message.from_user.id, message.contact.first_name, message.contact.last_name,
                                   message.contact.phone_number)
    # print(message.from_user.id, message.contact.first_name, message.contact.last_name,message.contact.phone_number)
    if response.status_code == 200:
        await message.answer("Поздравляем, вы зарегистрированы!")
    elif response.status_code == 422:
        await message.answer("Ошибка регистрации.")

    # Здесь добавить логику для получения и передачи телефонного номера в функцию check_user

    '''if not is_blocked:
        await send_message("Для создания заказа нажмите 'Создать заказ'. Для работы с текущими заказами нажмите 'Текущие заказы'.", message.chat.id)

        # Создаем клавиатуру с кнопками "Создать заказ" и "Текущие заказы"
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        button_create_order = KeyboardButton("Создать заказ")
        button_current_orders = KeyboardButton("Текущие заказы")
        keyboard.add(button_create_order, button_current_orders)

        await message.answer("Для создания заказа нажмите 'Создать заказ'. Для работы с текущими заказами нажмите 'Текущие заказы'.", reply_markup=keyboard)
'''


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
