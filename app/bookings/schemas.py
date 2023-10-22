from datetime import date

from pydantic import BaseModel, ConfigDict


class SchBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)


class SchGetBookings(BaseModel):
    id: int  # for booking
    room_id: int  # for booking
    user_id: int  # for booking
    date_from: date  # for booking
    date_to: date  # for booking
    price: int  # for booking
    total_cost: int  # for booking
    total_days: int  # for booking
    image_id: int  # for room
    name: str  # for room
    description: str  # for room
    services: list  # for room
