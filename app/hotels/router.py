import asyncio
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Path, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SchHotel, SchHotelByLocation

router = APIRouter(
    prefix='/hotels',
    tags=['Hotels'],
)


@router.get('/{hotel_id}')
async def get_hotel_by_id(hotel_id: int) -> SchHotel:
    return await HotelDAO.get_by_id(model_id=hotel_id)


@router.get('/loc/{location}', response_model=SchHotelByLocation)
@cache(expire=60)
async def get_hotel_by_location_and_time(
        location: Annotated[str, Path(examples='Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20')],
        date_from: Annotated[date, Query(examples='2023-05-15')],
        date_to: Annotated[date, Query(examples='2023-06-15')]
) -> SchHotelByLocation:
    await asyncio.sleep(3)
    return await HotelDAO.get_hotels_by_location_and_time(
        location=location,
        date_from=date_from,
        date_to=date_to,
    )


# @router.get('/loc/', response_model=SchHotelByLocation)
# async def get_hotel_by_location_and_time(
#         location: Annotated[str, Query(examples='Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20')],
#         date_from: Annotated[date, Query(example='2023-05-15')],
#         date_to: Annotated[date, Query(example='2023-06-15')]
# ) -> SchHotelByLocation:
#     return await HotelDAO.get_hotels_by_location_and_time(
#         location=location,
#         date_from=date_from,
#         date_to=date_to,
#     )
