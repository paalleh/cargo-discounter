from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from backend.services.offer_service import OfferService
from backend.schemas.offer import SchemaOffer

offer_router = APIRouter(prefix='/offer')

offer_router.tags = ["Offer"]

offer_service = OfferService()


@offer_router.post("/", response_model=SchemaOffer)
async def add_offer(new_offer: SchemaOffer):
    offer = await offer_service.add_offer(new_offer=new_offer)

    if type(offer) is Exception:
        raise HTTPException(status_code=400, detail=str(offer))

    return offer


@offer_router.get("/all_offers_for_order/{order_id}", response_model=List[SchemaOffer])
async def all_offers(order_id: int):
    offers = await offer_service.offers_by_order_id(order_id=order_id)

    if type(offers) is Exception:
        raise HTTPException(status_code=400, detail=str(offers))

    return offers


@offer_router.get("/offer_details/{offer_id}", response_model=SchemaOffer)
async def offer_details(offer_id: int):
    offer = await offer_service.offer_details(offer_id=offer_id)

    if type(offer) is Exception:
        raise HTTPException(status_code=400, detail=str(offer))

    return offer
