#регистрация.
from aiogram import F, Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg_bot_driver.settings.driver_bot_settings import bot_settings
from tg_bot_driver.backend_service.backend_service import backend_service
from tg_bot_driver.backend_service.driver_status import StatusDriver
from tg_bot_driver.keyboards.registr_keyboard import registr_keyboard
from tg_bot_driver.keyboards.main_keyboard import main_keyboard
from tg_bot_driver.keyboards.edit_profile_keyboard import edit_profile_keyboard

dp = Dispatcher()
bot = Bot(bot_settings.BOT_DRIVER_TOKEN)


class NewDriver(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    location = State()
    driver_license = State()

class UpdateDriver(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    location = State()
    driver_license = State()

driver_router = Router()
dp.include_router(driver_router)


@dp.message(CommandStart())
async def command_start_handler(message):
    await message.answer("Я работаю !")
    is_driver_exist = await backend_service.check_driver(int(message.from_user.id))

    match is_driver_exist:
        case StatusDriver.error:
            await message.answer(
                bot_settings.error_message
            )
        case StatusDriver.exist:
            await message.answer(
                bot_settings.greeting_message_registered,
                reply_markup=main_keyboard
            )
        case StatusDriver.not_exist:
            await message.answer(
                bot_settings.greeting_message_unregistered,
                reply_markup=registr_keyboard
            )
        case StatusDriver.not_full_profile:
            await message.answer(
                bot_settings.not_full_profile,
                reply_markup=registr_keyboard
            )


@dp.message(F.text.lower() == "зарегистрироваться")
async def registration(message: types.Message, state: FSMContext):
    await state.set_state(NewDriver.first_name)
    await message.answer("Введите имя: ")


@driver_router.message(NewDriver.first_name)
async def process_first_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(first_name=message.text)
    await state.set_state(NewDriver.last_name)

    await message.answer("Введите фамилию: ")


@driver_router.message(NewDriver.last_name)
async def process_last_name(message: types.Message, state: FSMContext) -> None:
    await state.update_data(last_name=message.text)
    await state.set_state(NewDriver.phone)

    await message.answer("Введите номер телефона: ")


@driver_router.message(NewDriver.phone)
async def process_phone(message: types.Message, state: FSMContext) -> None:
    await state.update_data(phone=message.text)
    await state.set_state(NewDriver.location)

    await message.answer("Введите геолокацию:")


@driver_router.message(NewDriver.location)
async def process_location(message: types.Message, state: FSMContext) -> None:
    await state.update_data(location=message.text)
    await state.set_state(NewDriver.driver_license)

    await message.answer("Введите водительские права: ")


@driver_router.message(NewDriver.driver_license)
async def process_driver_license(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(driver_license=message.text)
    await state.clear()
    data["id"] = message.from_user.id
    await backend_service.update_driver(data=data)

    await message.answer("Регистрация прошла успешно! ")


@dp.message(F.text.lower() == "мой профиль")
async def get_profile(message: types.Message):
    profile = await backend_service.get_driver(driver_id=message.from_user.id)

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
                case "location":
                    key = "Геолокация"
                case "driver_license":
                    key = "Водительские права"

            msg += f"{key}: {value}\n"

    await message.answer(
        msg,
        reply_markup=edit_profile_keyboard
    )

@dp.callback_query(F.data == "edit_first_name")
async def edit_first_name(callback: types.CallbackQuery, state: FSMContext):
     await state.set_state(UpdateDriver.first_name)
     await callback.answer()
     await callback.message.answer("Введите новое имя: ")


@driver_router.message(UpdateDriver.first_name)
async def update_first_name(message: types.Message, state: FSMContext) -> None:
     data = await state.update_data(first_name=message.text)
     await state.clear()
     data["id"] = message.from_user.id
     await backend_service.update_driver(data=data)

     await message.answer("Имя успешно изменено")
     await get_profile(message)


@dp.callback_query(F.data == "edit_last_name")
async def edit_last_name(callback: types.CallbackQuery, state: FSMContext):
     await state.set_state(UpdateDriver.last_name)
     await callback.answer()
     await callback.message.answer("Введите новую фамилию: ")


@driver_router.message(UpdateDriver.last_name)
async def update_last_name(message: types.Message, state: FSMContext) -> None:
     data = await state.update_data(last_name=message.text)
     await state.clear()
     data["id"] = message.from_user.id
     await backend_service.update_driver(data=data)

     await message.answer("Фамилия успешно изменена")
     await get_profile(message)


@dp.callback_query(F.data == "edit_phone")
async def edit_phone(callback: types.CallbackQuery, state: FSMContext):
     await state.set_state(UpdateDriver.phone)
     await callback.answer()
     await callback.message.answer("Введите новый номер телефона: ")


@driver_router.message(UpdateDriver.phone)
async def update_phone(message: types.Message, state: FSMContext) -> None:
     data = await state.update_data(phone=message.text)
     await state.clear()
     data["id"] = message.from_user.id
     await backend_service.update_driver(data=data)

     await message.answer("Телефон успешно изменен")
     await get_profile(message)


@dp.callback_query(F.data == "edit_location")
async def edit_location(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateDriver.location)
    await callback.answer()
    await callback.message.answer("Введите новую геолокацию: ")


@driver_router.message(UpdateDriver.location)
async def update_location(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(location=message.text)
    await state.clear()
    data["id"] = message.from_user.id
    await backend_service.update_driver(data=data)

    await message.answer("Геолокация успешно изменена")
    await get_profile(message)


@dp.callback_query(F.data == "edit_driver_license")
async def edit_driver_license(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateDriver.driver_license)
    await callback.answer()
    await callback.message.answer("Введите новые водительские права: ")


@driver_router.message(UpdateDriver.driver_license)
async def update_driver_license(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(driver_license=message.text)
    await state.clear()
    data["id"] = message.from_user.id
    await backend_service.update_driver(data=data)

    await message.answer("Водительские права успешно изменены")
    await get_profile(message)

if __name__ == '__main__':
    print("Bot start polling!")
    dp.run_polling(bot)
