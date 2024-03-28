from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from handlers import router
from logger import LoggerSetup
import logging

logger_setup = LoggerSetup()
LOGGER = logging.getLogger(__name__)


def get_application() -> FastAPI:
    application = FastAPI()
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(router)
    return application


app = get_application()
