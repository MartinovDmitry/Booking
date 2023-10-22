from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    booking: Mapped[list['Booking']] = relationship(back_populates='user')

    def __str__(self):
        return f'User: {self.email}'
