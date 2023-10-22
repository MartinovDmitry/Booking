import time
import sentry_sdk

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.rooms.router import router as rooms_router
from app.users.router import router as users_router

app = FastAPI()

sentry_sdk.init(
    dsn="https://263bdaed1acd2d58eec8e8b9916394d9@o4505466613465088.ingest.sentry.io/4505987613589504",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app.mount("/static", StaticFiles(directory="app/static"), "static")

####################################################################################
# Exception handler
####################################################################################


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"Message": exc.errors()}),
    )


app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(rooms_router)
app.include_router(hotels_router)

app.include_router(pages_router)

app.include_router(images_router)


#############################################################################
# CORS
#############################################################################

origins = [
    'http"//localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

#############################################################################
# redis
#############################################################################


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        settings.redis_url, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")


##############################################################################
# SQLAdmin
##############################################################################

# admin = Admin(app, engine, authentication_backend=authentication_backend)
admin = Admin(
    app,
    engine,
)

admin.add_view(UserAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)
admin.add_view(BookingAdmin)

###############################################################################
# middleware
###############################################################################


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        "Request handling time",
        extra={
            "process_time": round(process_time, 4),
        },
    )
    return response
