import os


class SettingsURL:
    TOKEN = os.getenv("BOT_DRIVER_TOKEN")
    BASE_TG_DRIVER_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"