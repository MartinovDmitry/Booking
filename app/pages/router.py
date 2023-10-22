from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotel_by_id, get_hotel_by_location_and_time

router = APIRouter(
    prefix='/pages',
    tags=['Frontend'],
)

templates = Jinja2Templates(directory='app/templates')


@router.get('/hotels')
async def get_hotels_page(
        request: Request,
        hotel=Depends(get_hotel_by_id),
):
    return templates.TemplateResponse(
        name='hotels.html',
        context={'request': request, 'hotel': hotel},
    )
