from pydantic import BaseModel


class SchListOfRooms(BaseModel):
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int
    id: int
    total_cost: int
    rooms_left: int
