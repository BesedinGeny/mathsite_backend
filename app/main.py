import uvicorn as uvicorn

from app.conf.settings import settings

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


def run():
    if settings.ON_PRODUCTION:
        uvicorn.run(app,
                    host=settings.HOST,
                    port=settings.PORT)
    else:
        uvicorn.run("app:app", host=settings.HOST, port=settings.PORT, reload=True)


if __name__ == '__main__':
    run()
