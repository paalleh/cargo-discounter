from aiogram import F, Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from tg_bot_driver.settings.driver_bot_settings import bot_settings
from tg_bot_driver.backend_service.backend_service import backend_service
from tg_bot_driver.backend_service.driver_status import StatusDriver
from tg_bot_driver.backend_service.car_status import StatusCar
from tg_bot_driver.keyboards.registr_keyboard import registr_keyboard
from tg_bot_driver.keyboards.main_keyboard import main_keyboard
from tg_bot_driver.keyboards.edit_profile_keyboard import edit_profile_keyboard
from tg_bot_driver.keyboards.add_car_keyboard import add_car_keyboard
from tg_bot_driver.keyboards.edit_car_keyboard import edit_car_keyboard
from tg_bot_driver.keyboards.choose_car_keyboard import get_check_car_keyboard


dp = Dispatcher()
bot = Bot(bot_settings.BOT_DRIVER_TOKEN)


class NewDriver(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    location = State()
    driver_license = State()


class NewCar(StatesGroup):
    car_number = State()
    vendor = State()
    model = State()
    load_capacity = State()
    volume = State()


class UpdateCar(StatesGroup):
    position_id = State()
    car_number = State()
    vendor = State()
    model = State()
    load_capacity = State()
    volume = State()


class UpdateDriver(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()
    location = State()
    driver_license = State()


class AcceptOrder(StatesGroup):
    order_id = State()
    price = State()


driver_router = Router()
dp.include_router(driver_router)


car_router = Router()
dp.include_router(car_router)


@dp.message(CommandStart())
async def command_start_handler(message):
    await message.answer("Я работаю !")
    is_driver_exist = await backend_service.check_driver(int(message.from_user.id))
    is_car_exist = await backend_service.check_car(int(message.from_user.id))

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

    match is_car_exist:
        case StatusCar.error:
            await message.answer(
                bot_settings.error_message
            )
        case StatusCar.exist:
            await message.answer(
                bot_settings.car_registered,
                reply_markup=main_keyboard
            )
        case StatusCar.not_exist:
            await message.answer(
                bot_settings.greeting_message_unregistered,
                reply_markup=add_car_keyboard
            )
        case StatusCar.not_full_profile:
            await message.answer(
                bot_settings.not_full_profile,
                reply_markup=add_car_keyboard
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


@dp.message(F.text.lower() == "добавить автомобиль")
async def add_car(message: types.Message, state: FSMContext):
    await state.set_state(NewCar.car_number)
    await message.answer("Введите регистрационный номер автомобиля: ")


@car_router.message(NewCar.car_number)
async def add_car_number(message: types.Message, state: FSMContext) -> None:
    await state.update_data(car_number=message.text)
    await state.set_state(NewCar.vendor)

    await message.answer("Введите марку автомобиля: ")


@car_router.message(NewCar.vendor)
async def add_car_vendor(message: types.Message, state: FSMContext) -> None:
    await state.update_data(vendor=message.text)
    await state.set_state(NewCar.model)

    await message.answer("Введите модель автомобиля: ")


@car_router.message(NewCar.model)
async def add_car_model(message: types.Message, state: FSMContext) -> None:
    await state.update_data(model=message.text)
    await state.set_state(NewCar.load_capacity)

    await message.answer("Введите тип кузова:")


@car_router.message(NewCar.load_capacity)
async def add_car_load_capacity(message: types.Message, state: FSMContext) -> None:
    await state.update_data(load_capacity=float(message.text))
    await state.set_state(NewCar.volume)

    await message.answer("Введите объем кузова: ")


@car_router.message(NewCar.volume)
async def add_car_volume(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(volume=float(message.text))
    await state.clear()
    data["driver_id"] = message.from_user.id
    await backend_service.add_car(data=data)

    await message.answer("Автомобиль добавлен! ")


@dp.message(F.text.lower() == "мой гараж")
async def edit_car(message: types.Message):
    car_profile = await backend_service.get_car(driver_id=message.from_user.id)

    msg = "Список ваших автомобилей:\n"
    initial_id: int = 0

    for car in car_profile.json():
        msg += "\n"
        msg += f"Ваш авто N: {initial_id}\n\n"
        for key, value in car.items():
            if key != "car_id" and key != "driver_id":
                match key:
                    case "car_number":
                        key = "Регистрационный номер автомобиля"
                    case "vendor":
                        key = "Марка автомобиля"
                    case "model":
                        key = "Модель автомобиля"
                    case "load_capacity":
                        key = "Тип кузова"
                    case "volume":
                        key = "Объем"

                msg += f"{key}: {value}\n"
        initial_id += 1

    choose_car_keyboard = get_check_car_keyboard(len(car_profile.json()))

    await message.answer(
        msg,
        reply_markup=choose_car_keyboard
    )


@dp.callback_query(F.data.startswith("edit_my_car_"))
async def choose_car(callback: types.CallbackQuery, state: FSMContext):
    car_position_id_str = callback.data.replace("edit_my_car_", "")
    await state.set_state(UpdateCar.position_id)
    await state.update_data(position_id=car_position_id_str)
    await callback.answer()
    await callback.message.answer("Выберите параметры для редактирования", reply_markup=edit_car_keyboard)


@dp.callback_query(F.data == "edit_car_number")
async def edit_car_number(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCar.car_number)
    await callback.answer()
    await callback.message.answer("Введите новый регистрационный номер: ")


@dp.callback_query(F.data == "edit_vendor")
async def edit_vendor(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCar.vendor)
    await callback.answer()
    await callback.message.answer("Введите марку автомобиля: ")


@dp.callback_query(F.data == "edit_model")
async def edit_model(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCar.model)
    await callback.answer()
    await callback.message.answer("Введите модель автомобиля: ")


@dp.callback_query(F.data == "edit_load_capacity")
async def edit_load_capacity(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCar.load_capacity)
    await callback.answer()
    await callback.message.answer("Введите тип кузова: ")


@dp.callback_query(F.data == "edit_volume")
async def edit_volume(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UpdateCar.volume)
    await callback.answer()
    await callback.message.answer("Введите объем: ")


@driver_router.message(UpdateCar.car_number)
async def update_car_number(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(car_number=message.text)
    await state.clear()

    car_profile = await backend_service.get_car(driver_id=message.from_user.id)
    car = car_profile.json()[int(data["position_id"])]

    update_data = {"car_id": car["car_id"], "car_number": data["car_number"]}

    await backend_service.update_car(data=update_data)

    await message.answer("Регистрационный номер успешно изменен")
    await edit_car(message)


@driver_router.message(UpdateCar.vendor)
async def update_vendor(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(vendor=message.text)
    await state.clear()

    car_profile = await backend_service.get_car(driver_id=message.from_user.id)
    car = car_profile.json()[int(data["position_id"])]

    update_data = {"car_id": car["car_id"], "vendor": data["vendor"]}

    await backend_service.update_car(data=update_data)

    await message.answer("Марка успешно изменена")
    await edit_car(message)


@driver_router.message(UpdateCar.model)
async def update_model(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(model=message.text)
    await state.clear()

    car_profile = await backend_service.get_car(driver_id=message.from_user.id)
    car = car_profile.json()[int(data["position_id"])]

    update_data = {"car_id": car["car_id"], "model": data["model"]}

    await backend_service.update_car(data=update_data)

    await message.answer("Модель успешно изменена")
    await edit_car(message)


@driver_router.message(UpdateCar.load_capacity)
async def update_load_capacity(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(load_capacity=message.text)
    await state.clear()

    car_profile = await backend_service.get_car(driver_id=message.from_user.id)
    car = car_profile.json()[int(data["position_id"])]

    update_data = {"car_id": car["car_id"], "load_capacity": data["load_capacity"]}

    await backend_service.update_car(data=update_data)

    await message.answer("Тип кузова изменен")
    await edit_car(message)


@driver_router.message(UpdateCar.volume)
async def update_volume(message: types.Message, state: FSMContext) -> None:
    data = await state.update_data(volume=message.text)
    await state.clear()

    car_profile = await backend_service.get_car(driver_id=message.from_user.id)
    car = car_profile.json()[int(data["position_id"])]

    update_data = {"car_id": car["car_id"], "volume": data["volume"]}

    await backend_service.update_car(data=update_data)

    await message.answer("Объем кузова изменен")
    await edit_car(message)


@dp.callback_query(F.data.startswith("accept_"))
async def create_offer(callback: types.CallbackQuery, state: FSMContext):
    order_id = callback.data.replace("accept_", "")
    await state.set_state(AcceptOrder.order_id)
    await state.update_data(order_id=order_id)
    await state.set_state(AcceptOrder.price)

    await callback.answer()
    await callback.message.answer("Введите цену выполнения заказа:")


@driver_router.message(AcceptOrder.price)
async def confirm_offer(message: types.Message, state: FSMContext):
    data = await state.update_data(price=message.text)
    await state.clear()

    data["order_id"] = int(data["order_id"])
    data["price"] = float(data["price"])
    data["driver_id"] = int(message.from_user.id)

    await backend_service.create_order(data=data)
    await message.answer("Вы успешно откликнулись на заказ!")


if __name__ == '__main__':
    print("Bot start polling!")
    dp.run_polling(bot)
