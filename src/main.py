from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.api.api_v1.routers import api_router
from src.core.config import settings
from src.utils.app_exceptions import (
    AppExceptionCase,
    AppException,
    app_exception_handler,
)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request: Request, exc: AppException):
    return await app_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "body": exc.body,
                "your_additional_errors": {
                    "Will be": "Inside",
                    "This": " Error message",
                },
            }
        ),
    )


@app.get("/")
async def root():
    return {"response": "Hello, World!"}


app.include_router(api_router, prefix=settings.API_V1_STR)
