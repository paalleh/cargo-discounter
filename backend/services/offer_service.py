from typing import Type, List

from backend.crud.offer_crud import OfferCRUD
from backend.crud.order_crud import OrderCRUD
from backend.crud.driver_crud import DriverCRUD
from backend.schemas.offer import SchemaOffer
from backend.models.models import Offers


class OfferService:
    def __init__(self):
        self.offer_crud = OfferCRUD()
        self.order_crud = OrderCRUD()
        self.driver_crud = DriverCRUD()

    async def __offer_model_to_offer_schema(self, offer: Type[Offers]) -> SchemaOffer:
        offer_schema = SchemaOffer(
            id=offer.id,
            order_id=offer.order_id,
            driver_id=offer.driver_id,
            price=offer.price
        )

        return offer_schema

    async def add_offer(self, new_offer: SchemaOffer) -> SchemaOffer | Exception:
        for key, value in new_offer.dict().items():
            if value is None and key != "id":
                return Exception(f"Cannot be an empty {key} in the new offer")

        order = await self.order_crud.get_order_by_id(order_id=new_offer.order_id)
        if order is None:
            return Exception("Incorrect order_id")

        driver = await self.driver_crud.get_driver(driver_id=new_offer.driver_id)
        if driver is None:
            return Exception("Incorrect driver_id")

        offer = await self.offer_crud.add_offer(new_offer=new_offer)

        new_offer.id = offer.id
        return new_offer

    async def offer_details(self, offer_id: int) -> SchemaOffer | Exception:
        offer = await self.offer_crud.get_offer(offer_id=offer_id)

        if offer is None:
            return Exception("Incorrect offer_id")

        offer_schema = await self.__offer_model_to_offer_schema(offer=offer)
        return offer_schema

    async def offers_by_order_id(self, order_id: int) -> List[SchemaOffer] | Exception:
        order = await self.order_crud.get_order_by_id(order_id=order_id)
        if order is None:
            return Exception("Incorrect order_id")

        offers_model = await self.offer_crud.get_offer_list_by_order(order_id=order_id)
        offers_schema = []

        for offer_model in offers_model:
            offer_schema = await self.__offer_model_to_offer_schema(offer_model)
            offers_schema.append(offer_schema)

        return offers_schema
