from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = dict()

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = {'Message': 'User already exists'}


class IncorrectEmailOrPassword(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {'Message': 'Incorrect Email or Pass'}


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {'Message': 'Token\'s lifetime is expired'}


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {'Message': 'Token has gone'}


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {'Message': 'Token\'s format is not a JWT'}


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = {'Message': 'There is no user in database'}


class RoomCanNotBeBooked(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = {'Message': 'There is no empty rooms'}