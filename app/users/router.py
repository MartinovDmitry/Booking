from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response

from app.exceptions import IncorrectEmailOrPassword, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.schemas import SchGetUser, SchUserLogin, SchUserRegister

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/register')
async def register_user(user_data: SchUserRegister) -> dict:
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add_data(email=user_data.email, hashed_password=hashed_password)
    return {'Message': 'It is all done'}


@router.post('/login')
async def login_user(
        response: Response,
        user_data: SchUserLogin,
) -> dict:
    user = await authenticate_user(
        email=user_data.email,
        password=user_data.password,
    )
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return {'access_token': access_token}


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')
    return {'Message': 'User logout'}


@router.get('/me')
async def read_me(user: SchUserLogin = Depends(get_current_user)) -> SchGetUser:
    return user


@router.get('/all_users')
async def get_all_users(user: SchUserLogin = Depends(get_current_user)) -> list[SchGetUser]:
    return await UserDAO.get_all()
