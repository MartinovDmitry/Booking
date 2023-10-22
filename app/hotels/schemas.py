from pydantic import BaseModel, ConfigDict


class SchHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: int


class SchHotelByLocation(SchHotel):
    # quantity: int | None
    # rooms_booked: int | None
    rooms_left: int | None

    model_config = ConfigDict(from_attributes=True)
