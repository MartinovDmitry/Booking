import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_picture

router = APIRouter(
    prefix='/images',
    tags=['Upload Images']
)


@router.post('/hotels')
async def add_hotel_image(file_id: int, file: UploadFile):
    image_path = f'app/static/images/{file_id}.webp'
    with open(image_path, 'wb+') as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_picture.delay(image_path)


