from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.main_page.main_page_router import main_page_router
from handlers import router
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi



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
    application.include_router(main_page_router)
    return application


app = get_application()


@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="FastAPI API documentation")


@app.get("/api/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return get_openapi(title="FastAPI", version="1.0", routes=app.routes)
