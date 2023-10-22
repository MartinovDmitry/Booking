from datetime import date

from sqlalchemy import func, or_, select

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.models import Room


class RoomDAO(BaseDAO):
    model = Room

    @classmethod
    async def get_rooms(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        """
            with booked_rooms as (
            select * from bookings where date_from >= '2023-06-15' or date_to <= '2023-05-05')
            select rooms.id, hotel_id, name, description, services, rooms.price, quantity, image_id,
            (20) * rooms.price as total_cost, rooms.quantity - count(booked_rooms.room_id) as rooms_left from rooms
            left join booked_rooms on booked_rooms.room_id = rooms.id
            where rooms.hotel_id = '1'
            group by rooms.id, hotel_id, name, description, rooms.price, quantity, image_id
            order by rooms.id asc
        """
        async with async_session_maker() as session:
            booked_rooms = select(Booking).where(or_(Booking.date_from >= date_to, Booking.date_to <= date_from)).\
                cte('booked_rooms')
            rooms_left = select(
                Room.__table__.columns,
                ((date_to - date_from).days * Room.price).label('total_cost'),
                (Room.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left'),
            ).select_from(Room).join(
                booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True,
            ).where(Room.hotel_id == hotel_id).group_by(
                Room.id,
                Room.hotel_id,
                Room.name,
                Room.description,
                Room.price,
                Room.quantity,
                Room.image_id
            ).order_by(Room.id)

            result_rooms = await session.execute(rooms_left)
            rooms_left = result_rooms.mappings().fetchall()

            return rooms_left
