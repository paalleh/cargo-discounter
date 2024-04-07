from typing import Type, List

from fastapi_sqlalchemy import db

from backend.crud.db_operations import DBOperations
from backend.models.models import Offers
from backend.schemas.offer import SchemaOffer


class OfferCRUD(DBOperations):
    async def get_offer(self, offer_id: int) -> Type[Offers] | None:
        offer = db.session.query(Offers).filter(Offers.id == offer_id).first()
        return offer

    async def get_offer_list_by_order(self, order_id: int) -> list[Type[Offers]]:
        offers = db.session.query(Offers).filter(Offers.order_id == order_id).all()
        return offers

    async def add_offer(self, new_offer: SchemaOffer) -> Offers:
        offer = Offers(
            price=new_offer.price,
            order_id=new_offer.order_id,
            driver_id=new_offer.driver_id
        )

        await self.db_write(offer)

        return offer
