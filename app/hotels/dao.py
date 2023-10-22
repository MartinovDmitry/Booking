from datetime import date

from sqlalchemy import func, or_, select

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotel
from app.hotels.schemas import SchHotelByLocation
from app.rooms.models import Room


class HotelDAO(BaseDAO):
    model = Hotel

    @classmethod
    async def get_hotels_by_location_and_time(cls, location: str, date_from: date, date_to: date):
        """
            -- in '2023-05-15'
            -- out '2023-06-05'
            with booked_rooms as (
            select bookings.room_id, count(bookings.room_id) as rooms_booked, rooms.id, rooms.quantity, rooms.hotel_id
            from bookings left join rooms on rooms.id = bookings.room_id
            where bookings.date_from >= '2023-06-15' or bookings.date_to <= '2023-05-05'
            group by room_id, rooms.id, rooms.quantity
            )
            select hotels.id, hotels.name, hotels.location, hotels.rooms_quantity,
            booked_rooms.rooms_booked, booked_rooms.quantity, booked_rooms.quantity - booked_rooms.rooms_booked as rooms_left
            from hotels
            left join booked_rooms on hotels.id = booked_rooms.hotel_id
            where hotels.location = LOCATION
        """
        async with async_session_maker() as session:
            booked_rooms = select(
                Booking.room_id, func.count(Booking.room_id).label('rooms_booked'), Room.id, Room.quantity, Room.hotel_id
            ).where(or_(Booking.date_from >= date_to, Booking.date_to <= date_from)).\
                join(Room, Room.id == Booking.room_id).group_by(Booking.room_id, Room.id, Room.quantity)

            left_rooms = select(
                Hotel.__table__.columns,
                booked_rooms.c.quantity,
                booked_rooms.c.rooms_booked,
                (Hotel.rooms_quantity - booked_rooms.c.rooms_booked).label('rooms_left'),
            ).where(Hotel.location == location).join(Hotel, Hotel.id == booked_rooms.c.hotel_id, isouter=True)
            res_left_rooms = await session.execute(left_rooms)
            res = res_left_rooms.mappings().all()[0]

            if res['rooms_left'] < 1:
                return {'Message': 'There is no hotels with empty rooms'}
            return res
