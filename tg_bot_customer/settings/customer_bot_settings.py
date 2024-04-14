import os
from dotenv import load_dotenv


if os.path.exists('../.env'):
    load_dotenv('../.env')


class BotSettings:
    BOT_CUSTOMER_TOKEN = os.getenv("BOT_CUSTOMER_TOKEN")
    BASE_API_URL = os.getenv("BASE_API_URL")

    greeting_message_unregistered: str = """
    Здравствуйте, это бот cargo-discounter, 
    который позволяет быстро находить водителей для грузоперевозок.
    Перед использованием необходимо зарегистрироваться.
    """

    greeting_message_registered: str = """
    Добро пожаловать!
    """

    error_message: str = """
    Во время работы бота произошла ошибка. Наши специалисты уже работают над ней!
    """

    not_full_profile: str = """
    Заполните все данные в вашем профиле.
    """


bot_settings = BotSettings()
