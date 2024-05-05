from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers.reporting_system.reporting_system_router import reporting_system_page_router
from routers.student.student_router import student_router
from routers.team.team_router import team_router
from routers.registration_page.registration_router import registration_router
from routers.user.user_router import user_router
from routers.util.util_router import util_router
from routers.kr_page.kr_page_router import kr_page_router
from routers.speciality_comparison_page.speciality_comparison_page_router import \
    speciality_comparison_page_router
from routers.group_comparison_page.group_comparison_page_router import group_comparison_page_router
from routers.student_page.student_page_router import student_page_router
from routers.main_page.main_page_router import main_page_router
from routers.scatter_plot_page.scatter_plot_page_router import scatter_plot_page_router
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
    application.include_router(main_page_router)
    application.include_router(student_page_router)
    application.include_router(group_comparison_page_router)
    application.include_router(speciality_comparison_page_router)
    application.include_router(kr_page_router)
    application.include_router(reporting_system_page_router)
    application.include_router(util_router)
    application.include_router(user_router)
    application.include_router(registration_router)
    application.include_router(team_router)
    application.include_router(student_router)
    application.include_router(scatter_plot_page_router)
    return application


app = get_application()

@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="FastAPI API documentation")


@app.get("/api/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return get_openapi(title="FastAPI", version="1.0", routes=app.routes)
