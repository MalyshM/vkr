from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from models import User, async_session_users, connect_db_users
from routers.registration_page.registration_router import login_standard
from routers.util_funcs import get_current_user_dev
from schemas import UserRegistration, UserLogin
from starlette.requests import Request


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.isadmin, User.iscurator, User.isteacher, User.fio, User.email, User.username,
                   User.date_of_add, ]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        try:
            async with async_session_users() as db:
                query = await db.execute(f"""
                                select
                                *
                            from users u
                            where 
                                u.email = '{username}'
                                """)
                user = query.one()
        except:
            return False
        user_login = UserLogin(FIO=user.fio, username=user.username, password=password, email=user.email)
        db = async_session_users()
        token = await login_standard(user_login, request, db)
        db.close()
        user = await get_current_user_dev(token["access_token"])
        if user.isadmin:
            request.session.update({"token": token["access_token"]})
            return True
        else:
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        user = await get_current_user_dev(token)
        if user.isadmin:
            request.session.update({"token": token})
            return True
        else:
            return False
