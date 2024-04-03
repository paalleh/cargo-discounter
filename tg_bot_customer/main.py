import os
from dotenv import load_dotenv


if os.path.exists('../.env'):
    load_dotenv('../.env')

print(os.getenv("CUSTOMER_BOT_TOKEN"))
