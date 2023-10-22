from datetime import date

from sqlalchemy import and_, delete, insert, or_, select

from app.bookings.models import Booking
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.models import Room


class BookingDAO(BaseDAO):
    model = Booking

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        WITH booked_rooms AS (
        SELECT * from bookings
        WHERE room_id = 1 AND
        ((date_from >= '2033-06-20') OR
        (date_to >= '2033-05-15'))
        )
        SELECT rooms.quantity - count(booked_rooms.room_id) from rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = room_id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        :return:
        """
        async with async_session_maker() as session:
            booked_rooms = (
                select(Booking)
                .where(
                    and_(
                        Booking.room_id == 1,
                        or_(Booking.date_from >= date_to, Booking.date_to >= date_from),
                    )
                )
                .cte("booked_rooms")
            )
            from sqlalchemy import func

            rooms_left = (
                select(
                    Room.quantity
                    - func.count(booked_rooms.c.room_id).label("rooms_left")
                )
                .select_from(Room)
                .join(booked_rooms, booked_rooms.c.room_id == room_id, isouter=True)
                .where(Room.id == room_id)
                .group_by(Room.quantity, booked_rooms.c.room_id)
            )

            # print(rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))

            result_rooms = await session.execute(rooms_left)
            rums_left: int = result_rooms.scalar()
            print(rums_left)

            if rums_left > 0:
                get_price = select(Room.price).filter_by(id=room_id)
                result_price = await session.execute(get_price)
                price: int = result_price.scalar()
                add_booking = (
                    insert(Booking)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Booking)
                )
                result_booking = await session.execute(add_booking)
                await session.commit()
                return result_booking.scalar()
            else:
                return None

    @classmethod
    async def get_bookings(cls):
        """
        select room_id, user_id, date_from, date_to, bookings.price, total_cost, total_days,
        rooms.image_id, rooms.name, rooms.description, rooms.services from bookings
        left join rooms on rooms.id = bookings.room_id
        order by room_id
        """
        async with async_session_maker() as session:
            query = (
                select(
                    Booking.__table__.columns,
                    Room.image_id,
                    Room.name,
                    Room.description,
                    Room.services,
                )
                .join(Room, Room.id == Booking.room_id)
                .order_by(Booking.room_id)
            )
            result = await session.execute(query)

            return result.mappings().all()

    @classmethod
    async def delete_booking(cls, booking_id: int):
        """
        delete from bookings where id == 7
        """
        async with async_session_maker() as session:
            stmt = delete(Booking).where(Booking.id == booking_id).returning(Booking.id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
