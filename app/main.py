import uvicorn as uvicorn
from fastapi_jwt_auth import AuthJWT
from fastapi_pagination import add_pagination

from app.conf.settings import cookies_settings, settings

from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException

from app.routers.api import api_router
from app.routers.exception_handler import authjwt_exception_handler

app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    exception_handlers={AuthJWTException: authjwt_exception_handler},
)


app.include_router(api_router, prefix=settings.API_V1_STR)


add_pagination(app)


origins = [
    "http://localhost",
    "http://0.0.0.0",

    "http://localhost:8080",
    "http://0.0.0.0:8080"
]


@AuthJWT.load_config
def get_config():
    return cookies_settings


def run():
    if settings.ON_PRODUCTION:
        uvicorn.run(app,
                    host=settings.HOST,
                    port=settings.PORT)
    else:
        uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)


if __name__ == '__main__':
    run()
