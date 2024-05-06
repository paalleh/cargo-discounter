import os


class SettingsURL:
    DRIVER_TOKEN = os.getenv("BOT_DRIVER_TOKEN")
    BASE_TG_DRIVER_URL = f"https://api.telegram.org/bot{DRIVER_TOKEN}/sendMessage"
    CUSTOMER_TOKEN = os.getenv("BOT_CUSTOMER_TOKEN")
    BASE_TG_CUSTOMER_URL = f"https://api.telegram.org/bot{CUSTOMER_TOKEN}/sendMessage"
