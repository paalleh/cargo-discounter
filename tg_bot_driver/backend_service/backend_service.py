import requests

from tg_bot_driver.settings.driver_bot_settings import bot_settings
from tg_bot_driver.backend_service.driver_status import StatusDriver
from tg_bot_driver.backend_service.car_status import StatusCar


class BackandService:
    def __init__(self):
        self.base_url = bot_settings.BASE_API_URL
        self.driver_prefix = "driver/"
        self.car_prefix = "car/"
        self.offer_prefix = "offer/"

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
        requests.patch(url=self.base_url + self.driver_prefix, json=data)

    async def get_car(self, driver_id: int) -> requests.Response:
        response = requests.get(url=self.base_url + self.car_prefix + f"{driver_id}")
        return response

    async def check_car(self, car_id: int) -> StatusCar:
        car = await self.get_car(driver_id=car_id)
        if car.status_code == 400:
            await self.add_car(car_id)
            return StatusCar.not_exist
        elif car.status_code == 200:
            for value in car.json():
                if value is None:
                    return StatusCar.not_full_profile
            return StatusCar.exist
        else:
            return StatusCar.error

    async def add_car(self, data: dict[str, str | float]) -> None:
        requests.post(url=self.base_url + self.car_prefix, json=data)

    async def update_car(self, data: dict[str, str]) -> None:
        requests.patch(url=self.base_url + self.car_prefix, json=data)

    async def create_order(self, data: dict[str, int | float]) -> None:
        requests.post(url=self.base_url + self.offer_prefix, json=data)


backend_service = BackandService()
