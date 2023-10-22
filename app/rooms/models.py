from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Room(Base):
    __tablename__ = 'rooms'

    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[JSON] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column(nullable=True)

    bookings: Mapped[list['Booking']] = relationship(back_populates='room')
    hotel: Mapped['Hotel'] = relationship(back_populates='rooms')

    def __str__(self):
        return f'Room: {self.id}, name: {self.hotel}, price: {self.price}'
