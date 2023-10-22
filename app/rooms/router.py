from datetime import date
from typing import Annotated, Optional

from fastapi import APIRouter, Query

from app.database import async_session_maker
from app.rooms.dao import RoomDAO
from app.rooms.schemas import SchListOfRooms

router = APIRouter(
    prefix='/rooms',
    tags=['Rooms'],
)


@router.get('/{hotel_id}', response_model=list[SchListOfRooms])
async def get_rooms(
        hotel_id: int,
        date_from: Annotated[date, Query(examples='2023-05-15')],
        date_to: Annotated[date, Query(examples='2023-06-15')]
) -> list[SchListOfRooms]:
    return await RoomDAO.get_rooms(hotel_id, date_from, date_to)
