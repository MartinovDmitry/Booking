from sqladmin import ModelView

from app.bookings.models import Booking
from app.hotels.models import Hotel
from app.rooms.models import Room
from app.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.booking]
    column_details_exclude_list = [User.hashed_password]
    page_size = 5
    can_delete = False
    name = 'UserAdmin'
    name_plural = 'UsersAdmin'
    icon = 'fa-solid fa-user'


class HotelAdmin(ModelView, model=Hotel):
    column_list = '__all__'
    can_delete = False
    name = 'HotelAdmin'
    name_plural = 'HotelsAdmin'
    icon = 'fa-solid fa-hotel'


class RoomAdmin(ModelView, model=Room):
    column_list = '__all__'
    can_delete = False
    name = 'RoomAdmin'
    name_plural = 'RoomsAdmin'
    icon = 'fa-solid fa-bed'


class BookingAdmin(ModelView, model=Booking):
    column_list = '__all__'
    can_delete = False
    name = 'BookingAdmin'
    name_plural = 'BookingsAdmin'
    icon = 'fa-solid fa-book'
