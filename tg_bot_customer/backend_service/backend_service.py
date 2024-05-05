import requests

from tg_bot_customer.backend_service.customer_status import StatusCustomer
from tg_bot_customer.settings.customer_bot_settings import bot_settings


class BackendService:
    def __init__(self):
        self.base_url = bot_settings.BASE_API_URL
        self.customer_prefix = 'customer/'
        self.order_prefix = 'order/'

    async def get_customer(self, customer_id: int) -> requests.Response:
        response = requests.get(self.base_url + self.customer_prefix + f'?customer_id={customer_id}')

        return response

    async def update_customer(self, data: dict[str, str | bytes]):
        requests.patch(self.base_url + self.customer_prefix, json=data)

    async def check_customer(self, customer_id: int) -> StatusCustomer:
        customer = await self.get_customer(customer_id=customer_id)
        if customer.status_code == 400 and customer.json()["detail"] == "Customer doesn't exists":
            await self.create_customer(customer_id=customer_id)
            return StatusCustomer.not_exist
        elif customer.status_code == 200:
            for value in customer.json().values():
                if value is None:
                    return StatusCustomer.not_full_profile
            return StatusCustomer.exist
        else:
            return StatusCustomer.error

    async def create_customer(self, customer_id: int):
        data = {
            "id": customer_id
        }
        requests.post(self.base_url + self.customer_prefix, json=data)

    async def create_order(self, data: dict[str, str | float]):
        requests.post(self.base_url + self.order_prefix, json=data)


backend_service = BackendService()
