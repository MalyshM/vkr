from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from admin import UserAdmin, AdminAuth, ETLView
from models import engine
from routers.reporting_system.reporting_system_router import reporting_system_page_router
from routers.student.student_router import student_router
from routers.team.team_router import team_router
from routers.registration_page.registration_router import registration_router
from routers.top_10_most_and_least_page.top_10_most_and_least_page_router import top_10_most_and_least_page_router
from routers.user.user_router import user_router
from routers.util.util_router import util_router
from routers.kr_page.kr_page_router import kr_page_router
from routers.speciality_comparison_page.speciality_comparison_page_router import \
    speciality_comparison_page_router
from routers.group_comparison_page.group_comparison_page_router import group_comparison_page_router
from routers.student_page.student_page_router import student_page_router
from routers.main_page.main_page_router import main_page_router
from routers.scatter_plot_page.scatter_plot_page_router import scatter_plot_page_router
from routers.lagging_students_page.lagging_students_page_router import lagging_students_page_router
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqladmin import Admin

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
    application.include_router(lagging_students_page_router)
    application.include_router(top_10_most_and_least_page_router)
    return application


app = get_application()
authentication_backend = AdminAuth(secret_key='asdasdasd')
admin = Admin(app, engine, authentication_backend=authentication_backend, templates_dir="templates")
# admin = Admin(app, engine, base_url= '/admin/admin')
admin.add_view(UserAdmin)
admin.add_view(ETLView)

@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="FastAPI API documentation")


@app.get("/api/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return get_openapi(title="FastAPI", version="1.0", routes=app.routes)
