from aiogram import F, Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg_bot_customer.settings.customer_bot_settings import bot_settings
from tg_bot_customer.backend_service.backend_service import backend_service
from tg_bot_customer.backend_service.customer_status import StatusCustomer
from tg_bot_customer.keyboards.registr_keyboard import registr_keyboard
from tg_bot_customer.keyboards.main_keyboard import main_keyboard
from tg_bot_customer.keyboards.edit_profile_keyboard import edit_profile_keyboard

dp = Dispatcher()
bot = Bot(bot_settings.BOT_CUSTOMER_TOKEN)


class NewCustomer(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()


class UpdateCustomer(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()


customer_router = Router()
dp.include_router(customer_router)


@dp.message(CommandStart())
async def command_start_handler(message):
    is_customer_exist = await backend_service.check_customer(int(message.from_user.id))

    match is_customer_exist:
        case StatusCustomer.error:
            await message.answer(
                bot_settings.error_message
            )
        case StatusCustomer.exist:
            await message.answer(
                bot_settings.greeting_message_registered,
                reply_markup=main_keyboard
            )
        case StatusCustomer.not_exist:
            await message.answer(
                bot_settings.greeting_message_unregistered,
                reply_markup=registr_keyboard
            )
        case StatusCustomer.not_full_profile:
            await message.answer(
                bot_settings.not_full_profile,
                reply_markup=registr_keyboard
            )


@dp.message(F.text.lower() == "зарегистрироваться")
async def registration(message: types.Message, state: FSMContext):
    await state.set_state(NewCustomer.first_name)
    await message.answer("Введите имя: ")


@customer_router.message(NewCustomer.first_name)
async def process_first_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(NewCustomer.last_name)

    await message.answer("Введите фамилию: ")


@customer_router.message(NewCustomer.last_name)
async def process_last_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(NewCustomer.phone)

    await message.answer("Введите номер телефона: ")


@customer_router.message(NewCustomer.phone)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(phone=message.text)
    await state.clear()
    data["id"] = message.from_user.id
    await backend_service.update_customer(data=data)

    await message.answer("Регистрация успешно завершена", reply_markup=main_keyboard)


@dp.message(F.text.lower() == "мой профиль")
async def get_profile(message: types.Message):
    profile = await backend_service.get_customer(customer_id=message.from_user.id)

    msg = ""
    for key, value in profile.json().items():
        if key != "id" and key != "is_blocked":
            match key:
                case "first_name":
                    key = "Имя"
                case "last_name":
                    key = "Фамилия"
                case "phone":
                    key = "Номер телефона"

            msg += f"{key}: {value}\n"

    await message.answer(
        msg,
        reply_markup=edit_profile_keyboard
    )


@dp.callback_query(F.data == "edit_first_name")
async def edit_first_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCustomer.first_name)
    await callback.answer()
    await callback.message.answer("Введите новое имя: ")


@customer_router.message(UpdateCustomer.first_name)
async def update_first_name(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(first_name=message.text)
    await state.clear()
    data["id"] = message.from_user.id
    await backend_service.update_customer(data=data)

    await message.answer("Имя успешно изменено")
    await get_profile(message)


@dp.callback_query(F.data == "edit_last_name")
async def edit_last_name(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCustomer.last_name)
    await callback.answer()
    await callback.message.answer("Введите новую фамилию: ")


@customer_router.message(UpdateCustomer.last_name)
async def update_last_name(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(last_name=message.text)
    await state.clear()
    data["id"] = message.from_user.id
    await backend_service.update_customer(data=data)

    await message.answer("Фамилия успешно изменена")
    await get_profile(message)


@dp.callback_query(F.data == "edit_phone")
async def edit_phone(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCustomer.phone)
    await callback.answer()
    await callback.message.answer("Введите новый номер телефона: ")


@customer_router.message(UpdateCustomer.phone)
async def update_phone(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(phone=message.text)
    await state.clear()
    data["id"] = message.from_user.id
    await backend_service.update_customer(data=data)

    await message.answer("Телефон успешно изменен")
    await get_profile(message)


if __name__ == '__main__':
    print("Bot start polling!")
    dp.run_polling(bot)
