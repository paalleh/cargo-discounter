import os
from dotenv import load_dotenv


if os.path.exists('../.env'):
    load_dotenv('../.env')


class BotSettings:
    BOT_DRIVER_TOKEN = os.getenv("BOT_DRIVER_TOKEN")
    BASE_API_URL = os.getenv("BASE_API_URL")

    greeting_message_unregistered: str = """
    Здравствуйте, это бот cargo-discounter,
    который позволяет быстро находить водителей для грузоперевозок.
    Перед использованием необходимо зарегистрироваться.
    """

    greeting_message_registered: str = """
    Добро пожаловать! Ваш профиль активен
    """
    car_registered: str = """
    Профиль вашего автомобиля заполнен!
    """

    error_message: str = """
    Во время работы бота произошла ошибка. Наши специалисты уже работают над ней!
    """

    not_full_profile: str = """
    Заполните все данные в вашем профиле.
    """


bot_settings = BotSettings()
