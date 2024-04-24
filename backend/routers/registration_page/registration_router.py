import time
from datetime import timedelta, datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from logger import LOGGER
from models import connect_db_users, User
from routers.util_funcs import create_access_token, Hasher
from schemas import UserRegistration, UserLogin

registration_router = APIRouter(tags=["Registration/login page"])
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@registration_router.post('/api/registration_standard', name='Registration:registration_standard',
                          status_code=status.HTTP_200_OK,
                          description=
                          """
                                  Получает UserRegistration
                                  class UserRegistration(BaseModel):
                                      FIO: str
                                      username: str
                                      password: str
                                      email: str
                                      isAdmin: bool
                                      isTeacher: bool
                                      isCurator: bool
                                  (по сути просто словарь с ключами FIO, username и тд)
                                  Raises:
                                      Если юзер есть, то  raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с такими данными уже существует(юзернейм, е-мейл)")
             
                                  Returns:
                                      {"access_token": access_token, "token_type": "bearer"}
                                 \n
                                 {
                                   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJGSU8iOiJzdHJpbmciLCJpc0FkbWluIjp0cnVlLCJpc0N1cmF0b3IiOnRydWUsImlzVGVhY2hlciI6dHJ1ZSwidXNlcm5hbWUiOiJzdHJpbmciLCJwYXNzd29yZCI6InN0cmluZyIsImVtYWlsIjoic3RyaW5nIiwiZXhwIjoxNzA1MDcwNzU5fQ.WZShrhvSyHaGFvEumrcQh86CVg3m4wa7O_-tfmlhXNI",
                                   "token_type": "bearer"
                                 }
                          """)
async def registration_standard(user: UserRegistration, db: AsyncSession = Depends(connect_db_users)):
    start_time = time.time()
    href = f"registration_standard-{user}"
    LOGGER.info(f"{href} start")
    try:
        query = await db.execute(f"""
            select
                *
            from users u
            where 
                u.username ='{user.username}' and
                u.email = '{user.email}'
        """)
        check_user = query.first()
        if check_user is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Пользователь с такими данными уже существует(юзернейм, емейл)")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"FIO": user.FIO, "isAdmin": user.isAdmin, "isCurator": user.isCurator, "isTeacher": user.isTeacher,
                  "username": user.username, "password": user.password, "email": user.email},
            expires_delta=access_token_expires
        )
        db.add(
            User(isadmin=user.isAdmin, iscurator=user.isCurator, isteacher=user.isTeacher, fio=user.FIO,
                 username=user.username, password=Hasher.get_password_hash(user.password), email=user.email,
                 date_of_add=datetime.now().date()))
        LOGGER.info(f"{href} finish {(time.time() - start_time)}")
        await db.commit()
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        LOGGER.error(f"{href} Error {e.detail}")
        raise e
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@registration_router.post('/api/login_standard', name='Registration:login_standard', status_code=status.HTTP_200_OK,
                          description=
                          """
                                  Получает UserLogin
                                  class UserLogin(BaseModel):
                                      FIO: str
                                      username: str
                                      password: str
                                      email: str
                                  (по сути просто словарь с ключами FIO, username и тд)
                                  Raises:
                                      Если юзера нет, то  raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Нельзя войти в несуществующий аккаунт/Неправильно введены данные")
                                      Если пароль не трушный, то raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                         detail="Нельзя войти в несуществующий аккаунт/Неправильно введены данные")
                                  Returns:
                                      {"access_token": access_token, "token_type": "bearer"}
                                  \n
                                  {
                                   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJGSU8iOiJzdHJpbmciLCJpc0FkbWluIjp0cnVlLCJpc0N1cmF0b3IiOnRydWUsImlzVGVhY2hlciI6dHJ1ZSwidXNlcm5hbWUiOiJzdHJpbmciLCJwYXNzd29yZCI6IiQyYiQxMiREQ3RoSThzUkg1Mm03YXgwYzhyMUQuaEFzSExMcDQuS215NWN2ZUFvWU5PZVluV2F5a1M3ZSIsImVtYWlsIjoic3RyaW5nIiwiZXhwIjoxNzA1MDcwOTMxfQ.7L9hmvkX3hczvzgxkKyxhR0Gntkv1WGfEw4nnVDdfbc",
                                   "token_type": "bearer"
                                  }
                          """)
async def login_standard(user: UserLogin, db: AsyncSession = Depends(connect_db_users)):
    start_time = time.time()
    href = f"login_standard-{user}"
    LOGGER.info(f"{href} start")
    try:
        query = await db.execute(f"""
            select
                *
            from users u
            where 
                u.username ='{user.username}' and
                u.email = '{user.email}'
            """)
        check_user = query.first()
        if check_user is None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Нельзя войти в несуществующий аккаунт/Неправильно введены данные")
        is_true_login = Hasher.verify_password(user.password, check_user.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"FIO": check_user.fio, "isAdmin": check_user.isadmin, "isCurator": check_user.iscurator,
                  "isTeacher": check_user.isteacher,
                  "username": check_user.username, "password": check_user.password, "email": check_user.email},
            expires_delta=access_token_expires
        )
        if is_true_login:
            LOGGER.info(f"{href} finish {(time.time() - start_time)}")
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Нельзя войти в несуществующий аккаунт/Неправильно введены данные")
    except HTTPException as e:
        LOGGER.error(f"{href} Error {e.detail}")
        raise e
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
