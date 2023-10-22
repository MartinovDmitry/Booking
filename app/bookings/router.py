from datetime import date
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from pydantic import TypeAdapter, parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SchBooking, SchGetBookings
from app.exceptions import RoomCanNotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.schemas import SchUserLogin

router = APIRouter(
    prefix='/bookings',
    tags=['Bookings'],
)


@router.get('/')
async def get_bookings(user: SchUserLogin = Depends(get_current_user)) -> list[SchGetBookings]:
    return await BookingDAO.get_bookings()


@router.post('/')
async def add_booking(
        room_id: int,
        date_from: Annotated[date, Query(example='2023-05-15')],
        date_to: Annotated[date, Query(example='2023-06-15')],
        background_tasks: BackgroundTasks,
        user: SchUserLogin = Depends(get_current_user),
) -> SchBooking:
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    booking_dict = parse_obj_as(SchBooking, booking).model_dump()
    if not booking:
        raise RoomCanNotBeBooked
    # With celery
    # send_booking_confirmation_email.delay(booking=booking_dict, email_to=user.email)
    # With BackgroundTasks
    background_tasks.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking_dict


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: SchUserLogin = Depends(get_current_user)) -> None:
    return await BookingDAO.delete_booking(booking_id=booking_id)
