from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    created_booking = await BookingDAO.add(
        user_id=1,
        room_id=2,
        date_from=datetime.strptime('2023-07-15', '%Y-%m-%d'),
        date_to=datetime.strptime('2023-07-24', '%Y-%m-%d')
    )
    assert created_booking.user_id == 1
    assert created_booking.room_id == 2

    get_booking = await BookingDAO.get_by_id(created_booking.id)
    assert get_booking.id == created_booking.id
    