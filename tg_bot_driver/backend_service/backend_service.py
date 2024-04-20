import requests

from tg_bot_driver.settings.driver_bot_settings import bot_settings
from tg_bot_driver.backend_service.driver_status import StatusDriver


class BackandService:
    def __init__(self):
        self.base_url = bot_settings.BASE_API_URL
        self.driver_prefix = "driver/"

    async def get_driver(self, driver_id: int) -> requests.Response:
        response = requests.get(url=self.base_url + self.driver_prefix + f"{driver_id}")
        return response

    async def check_driver(self, driver_id: int) -> StatusDriver:
        driver = await self.get_driver(driver_id=driver_id)
        if driver.status_code == 400:
            await self.create_driver(driver_id)
            return StatusDriver.not_exist
        elif driver.status_code == 200:
            for value in driver.json().values():
                if value is None:
                    return StatusDriver.not_full_profile
            return StatusDriver.exist
        else:
            return StatusDriver.error

    async def create_driver(self, driver_id: int) -> None:
        data = {"id": driver_id}
        requests.post(url=self.base_url + self.driver_prefix, json=data)

    async def update_driver(self, data: dict[str, str]) -> None:
        print(data)
        r = requests.patch(url=self.base_url + self.driver_prefix, json=data)
        print(r.status_code)
        print(r.content)


backend_service = BackandService()
