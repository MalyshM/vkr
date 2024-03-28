import io
import logging
import os
import random
import string
import time
from datetime import datetime, timedelta
from typing import Optional

import jwt
import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from fastapi.responses import StreamingResponse

from models import connect_db_data, connect_db_users, User, async_session_users
from schemas import UserRegistration, TokenData, UserLogin
from util import Hasher, get_urls

LOGGER = logging.getLogger(__name__)
router = APIRouter()
logging.getLogger('passlib').setLevel(logging.ERROR)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post('/api/registration_standard', name='Registration:registration_standard', status_code=status.HTTP_200_OK,
             tags=["Registration"], description=
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
    await db.commit()
    return {"access_token": access_token, "token_type": "bearer"}


async def get_user(username, email):
    async with async_session_users() as db:
        query = await db.execute(f"""
            select
            *
        from users u
        where 
            u.username ='{username}' and
            u.email = '{email}'
            """)
        user = query.one()
        return user


@router.post('/api/get_current_user_dev', name='User:get_current_user_dev', status_code=status.HTTP_200_OK,
             tags=["User"], description=
             """
                     Получает token юзера(строка)
                     
                     Raises:
                         Если юзера нет, то  raise credentials_exception
                         
                     Returns:
                         User
                     \n
                     {
                      "password": "$2b$12$DCthI8sRH52m7ax0c8r1D.hAsHLLp4.Kmy5cveAoYNOeYnWaykS7e",
                      "id": 5,
                      "isadmin": true,
                      "iscurator": true,
                      "email": "string",
                      "fio": "string",
                      "username": "string",
                      "isteacher": true,
                      "date_of_add": "2024-01-12T00:00:00"
                     }
             """)
async def get_current_user_dev(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Нерабочий токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        password: str = payload.get("password")
        email: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, password=password, email=email)
    except:
        raise credentials_exception
    user = await get_user(username=token_data.username, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


@router.get('/api/get_all_users', name='User:get_all_users', status_code=status.HTTP_200_OK, tags=["User"], description=
"""
        Returns:
            List of Users
        \n
        [
          {
            "password": "$2b$12$DCthI8sRH52m7ax0c8r1D.hAsHLLp4.Kmy5cveAoYNOeYnWaykS7e",
            "id": 5,
            "isadmin": true,
            "iscurator": true,
            "email": "string",
            "fio": "string",
            "username": "string",
            "isteacher": true,
            "date_of_add": "2024-01-12T00:00:00"
          },
          {
            "password": "$2b$12$vtIbx59Sh.GuN3MqijRmoO769ZfdSC3JStLkL5L9RH97Cw/aE81ja",
            "id": 6,
            "isadmin": true,
            "iscurator": true,
            "email": "strin1g",
            "fio": "strin1g",
            "username": "strin1g",
            "isteacher": true,
            "date_of_add": "2024-01-12T00:00:00"
          }
        ]
""")
async def get_all_users(db: AsyncSession = Depends(connect_db_users)):
    LOGGER.info("check logs")
    all_users = await db.execute("""
        Select *
        from users u
    """)
    return all_users.fetchall()


@router.get('/api/delete_all_users', name='User:delete_all_users', status_code=status.HTTP_200_OK, tags=["User"],
            description=
            """
                    Returns:
                        {"message": "All users deleted successfully"}
                    \n
                    {
                      "message": "All users deleted successfully"
                    }
            """)
async def delete_all_users(db: AsyncSession = Depends(connect_db_users)):
    await db.execute("""DELETE FROM users""")
    await db.commit()
    return {"message": "All users deleted successfully"}


async def delete_test_user():
    async with async_session_users() as db:
        await db.execute("""
            DELETE FROM users u
             where u.username = 'string' and 
             u.email = 'string' and 
             u.fio = 'string'
         """)
        await db.commit()
    return {"message": "test user deleted successfully"}


@router.post('/api/login_standard', name='Registration:login_standard', status_code=status.HTTP_200_OK,
             tags=["Registration"], description=
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
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Нельзя войти в несуществующий аккаунт/Неправильно введены данные")


@router.get('/api/get_teams_for_user', name='Team:get_teams_for_user', status_code=status.HTTP_200_OK,
            tags=["Team"], description=
            """
                    Получает токен
                    Raises:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")

                    Returns:
                        массив Team (Team.id, Team.name)
                    \n
                    [
                      {
                        "id": 17,
                        "name": "ПиОА П-06.02"
                      },
                      {
                        "id": 39,
                        "name": "ПиОА П-07.03"
                      },
            """)
async def get_teams_for_user(token: str, db: AsyncSession = Depends(connect_db_data)):
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = await db.execute("""
        select distinct t.id, t.name from team t
        """)
        return response.fetchall()
    elif user.isteacher:
        response = await db.execute(f"""
            select
                distinct t.id,
                t.name
            from
                team t
            where
                t.id in (
                select
                    distinct l.team_id
                from
                    lesson l
                where
                    l.teacher_id in (
                    select
                        distinct t.id
                    from
                        teacher t
                    where
                        t.name ilike '%{user_fio}%'))
        """)
        return response.fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


async def get_teams_for_user_private(token: str, db):
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = await db.execute("""
            select distinct t.id, t.name from team t
            """)
        return response.fetchall()
    elif user.isteacher:
        response = await db.execute(f"""
            select
                distinct t.id,
                t.name
            from
                team t
            where
                t.id in (
                select
                    distinct l.team_id
                from
                    lesson l
                where
                    l.teacher_id in (
                    select
                        distinct t.id
                    from
                        teacher t
                    where
                        t.name ilike '%{user_fio}%'))
            """)
        return response.fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


async def get_teams_for_param_private_without_lect(teacher_arr: list, db):
    return await db.execute(f"""
                        select
                            distinct t.id,
                            t.name
                        from
                            team t
                        where
                            t.id in (
                            select
                                distinct l.team_id
                            from
                                lesson l
                            where
                                l.teacher_id in (
                                select
                                    distinct t.id
                                from
                                    teacher t
                                where
                                    t.name = ANY(ARRAY{teacher_arr}))
                            and t.name not ilike '%л%');
                                """)


async def get_teams_for_user_private_without_lect(token: str, db):
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = await db.execute("""
            select
                distinct t.id,
                t."name"
            from
                team t
            where
                t."name" not ilike '%л%'
        """)
        return response.fetchall()
    elif user.isteacher:
        response = await db.execute(f"""
                    select
                        distinct t.id,
                        t.name
                    from
                        team t
                    where
                        t.id in (
                        select
                            distinct l.team_id
                        from
                            lesson l
                        where
                            l.teacher_id in (
                            select
                                distinct t.id
                            from
                                teacher t
                            where
                                t.name ilike '%{user_fio}%'))
                        and t.name not ilike '%л%'
                    """)
        return response.fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


@router.get('/api/get_teams_for_user_without_lect', name='Team:get_teams_for_user_without_lect',
            status_code=status.HTTP_200_OK,
            tags=["Team"], description=
            """
                    Получает токен
                    Raises:
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")

                    Returns:
                        массив Team (Team.id, Team.name)
                    \n
                    [
                      {
                        "id": 17,
                        "name": "ПиОА П-06.02"
                      },
                      {
                        "id": 39,
                        "name": "ПиОА П-07.03"
                      },
            """)
async def get_teams_for_user_without_lect(token: str, db: AsyncSession = Depends(connect_db_data)):
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = await db.execute("""
                select
                    distinct t.id,
                    t."name"
                from
                    team t
                where
                    t."name" not ilike '%л%'
            """)
        return response.fetchall()
    elif user.isteacher:
        response = await db.execute(f"""
                        select
                            distinct t.id,
                            t.name
                        from
                            team t
                        where
                            t.id in (
                            select
                                distinct l.team_id
                            from
                                lesson l
                            where
                                l.teacher_id in (
                                select
                                    distinct t.id
                                from
                                    teacher t
                                where
                                    t.name ilike '%{user_fio}%'))
                            and t.name not ilike '%л%'
                        """)
        return response.fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


@router.get('/api/get_student', name='Stud:get_stud', status_code=status.HTTP_200_OK, tags=["Stud"], description=
"""
        Получает id_stud: int
        Returns:
            Студент
        \n
        {
          "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
          "id": 2,
          "email": "stud0000278787@study.utmn.ru",
          "date_of_add": "2024-01-13T00:00:00",
          "name": "bcd765d44ffc513ca68a954f119ea527407c413e3486c7029ff0c5522343810a"
        }
""")
async def get_student(id_stud: int, db: AsyncSession = Depends(connect_db_data)):
    all_users = await db.execute(f"""
        select
            *
        from
            stud s
        where
            s.id = {id_stud}
	""")
    return all_users.fetchall()


@router.get('/api/get_router_paths', name='Util:Util', status_code=status.HTTP_200_OK,
            tags=["Util"], description=
            """
                    Получает id_team: int, id_stud: int
                    Returns:
                        response_list = []
                        response_list.append({'name': row['name'], 'cum_sum': cum_sum[-1], 'counter': row['counter'], 'isTest': temp})
                    \n
                    [
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных",
                        "cum_sum": 2,
                        "counter": 1,
                        "isTest": false
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных1",
                        "cum_sum": 4,
                        "counter": 2,
                        "isTest": false
                      },
            """)
async def get_router_paths():
    router_list = [{"path": route.path, "name": route.name} for route in router.routes]
    resp = []
    for item in router_list:
        if "Registration" not in item['name'] and "User" not in item['name'] \
                and "Team" not in item['name'] and "Stud" not in item['name'] \
                and "Reporting system" not in item['name'] and "Util" not in item['name']:
            resp.append(item['path'])
    return resp


@router.get('/api/get_all_specialities', name='Util:get_all_specialities', status_code=status.HTTP_200_OK,
            tags=["Util"], description=
            """
                    Получает token: str
                    Returns:
                        специальности 
                    \n
                    [
                      {
                        "speciality": "43.03.02 Туризм"
                      },
                      {
                        "speciality": "01.03.03 Механика и математическое моделирование"
                      },
                      {
                        "speciality": "35.03.10 Ландшафтная архитектура"
                      },
            """)
async def get_all_specialities(token: str, db: AsyncSession = Depends(connect_db_data)):
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = await db.execute("""
            select distinct
                s.speciality 
            from
                stud s 
        """)
        return response.fetchall()
    elif user.isteacher:
        response = await db.execute(f"""
            select distinct
                s.speciality 
            from
                stud s
            where
                s.id in (
                select
                    distinct l.stud_id
                from
                    lesson l
                where
                    l.teacher_id in (
                    select
                        distinct t.id
                    from
                        teacher t
                    where
                        t.name ilike '%{user_fio}%'))
        """)
        return response.fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


@router.get('/api/get_all_kr', name='Util:get_all_kr', status_code=status.HTTP_200_OK, tags=["Util"], description=
"""
        Returns:
            все кр
        \n
        [
          {
            "name": "Организация функций30"
          },
          {
            "name": "Коллекции. Работа с файлами20"
          },
          {
            "name": "Управляющие конструкции50"
          }
        ]
""")
async def get_all_kr(db: AsyncSession = Depends(connect_db_data)):
    all_users = await db.execute("""
        select distinct 
            l.name
        from
            lesson l
        where
            l.test >= 0.0
    """)
    return all_users.fetchall()


@router.get('/api/get_all_teachers_unique', name='Util:get_all_teachers', status_code=status.HTTP_200_OK,
            tags=["Util"], description=
            """
                    Получает token: str
                    Returns:
                        Преподаватели
                    \n
                    [
                      {
                        "id": 8,
                        "name": "Березовский Артем Константинович"
                      },
                      {
                        "id": 2,
                        "name": "Трефилин Иван Андреевич"
                      },
                      {
                        "id": 4,
                        "name": "Павлова Елена Александровна"
                      },
            """)
async def get_all_teachers_unique(token: str, db: AsyncSession = Depends(connect_db_data)):
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = await db.execute("""
            select distinct
                t.id,
                t."name"
            from
                teacher t
            where 
                t.name not ilike '%,%'
        """)
        return response.fetchall()
    elif user.isteacher:
        response = await db.execute(f"""
            select distinct
                t.id,
                t."name"
            from
                teacher t
            where
                t.name = '{user_fio}'
        """)
        return response.fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


@router.get('/api/get_all_teachers', name='Util:get_all_teachers', status_code=status.HTTP_200_OK,
            tags=["Util"], description=
            """
                    Получает token: str
                    Returns:
                        Преподаватели
                    \n
                    [
                      {
                        "id": 8,
                        "name": "Березовский Артем Константинович"
                      },
                      {
                        "id": 2,
                        "name": "Трефилин Иван Андреевич"
                      },
                      {
                        "id": 4,
                        "name": "Павлова Елена Александровна"
                      },
            """)
async def get_all_teachers(token: str, db: AsyncSession = Depends(connect_db_data)):
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = await db.execute("""
                select distinct
                    t.id,
                    t."name"
                from
                    teacher t
            """)
        return response.fetchall()
    elif user.isteacher:
        response = await db.execute(f"""
            select distinct
                t.id,
                t."name"
            from
                teacher t
            where
                t.name ilike '%{user_fio}%'
        """)
        return response.fetchall()
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


# Main page
# region
@router.get('/api/attendance_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Main page"], description=
            """
                    Получает команду по id
                    Returns:
                        массив словарей (Stud.name, Stud.id, Посещаемость)
                    \n
                    [
                      {
                        "name": "297fa3e7b1df9f4e503ff4b76a9806be595bc79c38687b7c2d0d6301ec8eb04e",
                        "id": 86,
                        "Посещаемость": 0.8636363636363636
                      },
                      {
                        "name": "391c01a02b6fd2ffd532b8ee8b3b8f6c91d3082f220680904b042469b3beaea1",
                        "id": 231,
                        "Посещаемость": 0.5
                      },
            """)
async def attendance_per_stud_for_team(id_team: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
        select distinct
            (select s.name from stud s where s.id=l.stud_id) as "stud_name",
            (select s.id from stud s where s.id=l.stud_id) as "stud_id",
            ROUND(count(id) filter (where l.arrival ='П') over (partition by stud_id) / count(id) over (partition by stud_id)::DECIMAL, 2) as "Посещаемость"
        from
            lesson l
        where
            l.team_id = {id_team}
    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/total_points_attendance_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Main page"], description=
            """
                    Получает команду по id
                    Returns:
                        массив словарей (Stud.name, Stud.id, Успеваемость, Посещаемость)
                    \n
                    [
                      {
                        "name": "297fa3e7b1df9f4e503ff4b76a9806be595bc79c38687b7c2d0d6301ec8eb04e",
                        "id": 86,
                        "Успеваемость": 77.5,
                        "Посещаемость": 86.36363636363636
                      },
                      {
                        "name": "391c01a02b6fd2ffd532b8ee8b3b8f6c91d3082f220680904b042469b3beaea1",
                        "id": 231,
                        "Успеваемость": 5.93,
                        "Посещаемость": 50
                      },
                      ...
                      {
                        "Stud_name": "ea8f90f44711633726715358e2a60d451b1123d91b75720276f82aecdd1fd6f9",
                        "Stud_id": 64,
                        "Успеваемость": 77.3,
                        "Посещаемость": 86.36363636363636
                      },
                      {
                        "total_points_avg": 67.72100005666667,
                        "arrival_avg": 77.8787878787879
                      }
            """)
async def total_points_attendance_per_stud_for_team(id_team: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
        select *, avg(sub.Успеваемость) over (partition by Посещаемость_средняя) as "Успеваемость_средняя"
        from
        (select distinct
            (select s.name from stud s where s.id=l.stud_id) as "stud_name",
            (select s.id from stud s where s.id=l.stud_id) as "stud_id",
            ROUND(count(id) filter (where l.arrival ='П') over (partition by stud_id) / count(id) over (partition by stud_id)::DECIMAL, 2) as "Посещаемость",
            ROUND((sum(l.mark_for_work) over (partition by stud_id) + sum(l.test) over (partition by stud_id))::DECIMAL, 2) as "Успеваемость",
            ROUND(count(id) filter (where l.arrival ='П') over (partition by team_id) / count(id) over (partition by team_id)::DECIMAL, 2) as "Посещаемость_средняя"
        from
            lesson l
        where
            l.team_id = {id_team}) as sub
    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/total_points_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Main page"], description=
            """
                    Получает команду по id
                    Returns:
                        массив словарей (Stud.name, Stud.id, Успеваемость)
                    \n
                    [
                      {
                        "name": "297fa3e7b1df9f4e503ff4b76a9806be595bc79c38687b7c2d0d6301ec8eb04e",
                        "id": 86,
                        "Успеваемость": 77.5
                      },
                      {
                        "name": "391c01a02b6fd2ffd532b8ee8b3b8f6c91d3082f220680904b042469b3beaea1",
                        "id": 231,
                        "Успеваемость": 5.93
                      },
            """)
async def total_points_per_stud_for_team(id_team: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
            select distinct
                (select s.name from stud s where s.id=l.stud_id) as "stud_name",
                (select s.id from stud s where s.id=l.stud_id) as "stud_id",
                ROUND((sum(l.mark_for_work) over (partition by stud_id) + sum(l.test) over (partition by stud_id))::DECIMAL, 2) as "Успеваемость"
            from
                lesson l
            where
                l.team_id = {id_team}
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/total_marks_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Main page"], description=
            """

                    Получает команду по id
                    Returns:
                        массив словарей 'avg_total_points', 'mark','percent'
                    \n
                    [
                      {
                        "avg_total_points": 10.879999925,
                        "mark": "неудовл.",
                        "percent": 0.13333333333333333
                      },
                      {
                        "avg_total_points": 62.515000333333326,
                        "mark": "удовл.",
                        "percent": 0.2
                      },
                      {
                        "avg_total_points": 77.5925,
                        "mark": "хор.",
                        "percent": 0.5333333333333333
                      },
                      {
                        "avg_total_points": 92.885,
                        "mark": "отл.",
                        "percent": 0.13333333333333333
                      }
                    ]
            """)
async def total_marks_for_team(id_team: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
        SELECT
            CASE
                WHEN Успеваемость > 60 AND Успеваемость < 76 THEN 'удовл.'
                WHEN Успеваемость > 75 AND Успеваемость < 91 THEN 'хор.'
                WHEN Успеваемость > 90 THEN 'отл.'
                ELSE 'неудовл.'
            END AS mark,
            ROUND(COUNT(*) / count_all::DECIMAL, 2) AS percent,
            ROUND(AVG(Успеваемость)::DECIMAL, 2) AS avg_total_points
        FROM
            (
            SELECT DISTINCT
                (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS stud_name,
                (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS stud_id,
                ROUND((SUM(l.mark_for_work) + SUM(l.test))::DECIMAL, 0) AS Успеваемость,
                (
                SELECT COUNT(DISTINCT stud_id) AS count_all 
                FROM lesson l
                WHERE l.team_id = {id_team}
                ) AS count_all
            FROM
                lesson l
            WHERE
                l.team_id = {id_team}
            GROUP BY 
                stud_id
            ) AS sub
        GROUP BY 
            mark, count_all;
    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/attendance_num_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Main page"], description=
            """
                    \nПолучает id_team: int\n
                    Returns:\n
                        массив словарей\n



                    [
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных",
                        "arrival": 23
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных1",
                        "arrival": 28
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных2",
                        "arrival": 28
                      },
                      {
                        "name": "Управляющие конструкции",
                        "arrival": 24
                      },
            """)
async def attendance_num_for_stud_for_team(id_team: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
        select 
            l.name,
            l.id,
            count(id) filter (where l.arrival ='П') over (partition by l.name) as "Посещаемость"
        from
            lesson l
        where
            l.team_id = {id_team}
        order by id
        limit 22
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/attendance_num_for_stud_for_team_stat_table', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Main page"], description=
            """
                    \nПолучает id_team: int, name_of_lesson: str\n
                    Returns:\n
                        массив словарей\n



                    [
                      {
                        "id": 1,
                        "Успеваемость": 50,
                        "Посещаемость": 93.33333333333333
                      },
                      {
                        "id": 30,
                        "Успеваемость": 9.5,
                        "Посещаемость": 26.666666666666668
                      },
            """)
async def attendance_num_for_stud_for_team_stat_table(id_team: int, name_of_lesson: str,
                                                      db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
        SELECT sub.stud_name, sub.id, sub.Посещаемость, sub.Успеваемость
        FROM (
          SELECT
            (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS stud_name,
            (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS id,
            l.name,
            ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL, 2) AS Посещаемость,
            ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) + SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW))::DECIMAL, 2) AS Успеваемость,
            l.arrival
          FROM
            lesson l
          WHERE
            l.team_id = {id_team}
        ) AS sub
        WHERE
          sub.name = '{name_of_lesson}' AND sub.arrival = 'Н';
            """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


# endregion

# Student page
# region
@router.get('/api/cum_sum_points_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Student page"], description=
            """
                    Получает id_team: int, id_stud: int
                    Returns:
                        response_list = []
                        response_list.append({'name': row['name'], 'cum_sum': cum_sum[-1], 'counter': row['counter'], 'isTest': temp})
                    \n
                    [
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных",
                        "cum_sum": 2,
                        "counter": 1,
                        "isTest": false
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных1",
                        "cum_sum": 4,
                        "counter": 2,
                        "isTest": false
                      },
            """)
async def cum_sum_points_for_stud_for_team(id_team: int, id_stud: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
            SELECT
                l.name,
                ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) + SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW))::DECIMAL, 2) AS cum_sum,
                row_number() over (PARTITION BY stud_id) as counter,
                CASE
                    WHEN l.test  >= 0 THEN false
                    ELSE true
                END AS test
              FROM
                lesson l
              WHERE
                l.team_id = {id_team} and l.stud_id = {id_stud}
                    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/attendance_dynamical_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Student page"], description=
            """
                    Получает id_team: int, id_stud: int
                    Returns:
                        response_list = []
                        response_list.append({'name': row['name'], 'dynamical_arrival': dynamical_arrival[-1] * 100})
                    \n
                    [
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных",
                        "dynamical_arrival": 100
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных1",
                        "dynamical_arrival": 100
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных2",
                        "dynamical_arrival": 100
                      },
            """)
async def attendance_dynamical_for_stud_for_team(id_team: int, id_stud: int,
                                                 db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
            SELECT
                l.name,
                ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL, 2) AS dynamical_arrival
              FROM
                lesson l
              WHERE
                l.team_id = {id_team} and l.stud_id = {id_stud}
                    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/attendance_static_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Student page"], description=
            """
                    Получает id_team: int, id_stud: int
                    Returns:
                        response_list = []
                        response_list.append({'name': row['name'], 'static_arrival': static_arrival[-1] * 100})
                    \n
                    [
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных",
                        "static_arrival": 4.545454545454546
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных1",
                        "static_arrival": 9.090909090909092
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных2",
                        "static_arrival": 13.636363636363635
                      },
            """)
async def attendance_static_for_stud_for_team(id_team: int, id_stud: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
            SELECT
                l.name,
                ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / COUNT(id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS static_arrival
              FROM
                lesson l
              WHERE
                l.team_id = {id_team} and l.stud_id = {id_stud}
                    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


@router.get('/api/all_in_one_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Student page"], description=
            """
                    Получает id_team: int, id_stud: int
                    Returns:
                        response_list = []
                        response_list.append({'name': row['name'], 'static_arrival': static_arrival[-1] * 100})
                    \n
                    [
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных",
                        "static_arrival": 4.545454545454546
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных1",
                        "static_arrival": 9.090909090909092
                      },
                      {
                        "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных2",
                        "static_arrival": 13.636363636363635
                      },
            """)
async def all_in_one_for_stud_for_team(id_team: int, id_stud: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    result_query = await db.execute(f"""
        SELECT
            l.name,
            ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL, 2) AS dynamical_arrival,
            ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / COUNT(id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS static_arrival,
            ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) + SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW))::DECIMAL, 2) AS cum_sum,
            row_number() over (PARTITION BY stud_id) as counter,
            CASE
                WHEN l.test  >= 0 THEN false
                ELSE true
            END AS test
          FROM
            lesson l
          WHERE
            l.team_id = {id_team} and l.stud_id = {id_stud}
                """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query.fetchall()


# endregion

# Group comparison page
# region
@router.get('/api/attendance_static_stud_for_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Group comparison page"], description=
            """
                    Получает id_team1: int, id_team2: int,
                    Returns:
                        [{'name': row[0], 'id': row[1], 'team_name': row[2], 'arrival': row[3], 'team_id': row[4]},...]
                    \n
                    [
                      {
                        "name": "7e69e519d8b8a86e5c1346ca6fc49a63bdd52c902978b7d67748f77d74979476",
                        "id": 859,
                        "team_name": "ПиОА П-08.02",
                        "arrival": 0.9545454545454546,
                        "team_id": 2
                      },
                      {
                        "name": "760abb57d6ed68ba2e3cca798a31217e8be9189fefa0bd89e215c6d700caeecd",
                        "id": 601,
                        "team_name": "ПиОА П-04.03",
                        "arrival": 1,
                        "team_id": 4
                      },
                      {
                        "name": "3c2e83fffbb983d214eb3a55ad18dafd12e4b5b8c993480c0a0b7453b786c2f9",
                        "id": 899,
                        "team_name": "ПиОА П-08.02",
                        "arrival": 0.9545454545454546,
                        "team_id": 2
                      },
                      {
                        "name": "cd5f76842f953535d5f545d258b8248c3f629ce1289aa7de074e47f05341152d",
                        "id": 553,
                        "team_name": "ПиОА П-04.03",
                        "arrival": 1,
                        "team_id": 4
                      },
            """)
async def attendance_static_stud_for_teams(id_team1: int, id_team2: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    res = await db.execute(f"""
        SELECT DISTINCT
            (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS name,
            (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS id,
            (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
            ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id) / COUNT(id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS static_arrival,
            (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id
        FROM
            lesson l
        WHERE
            l.team_id = {id_team1} OR l.team_id = {id_team2}
        order by static_arrival desc
    """)
    mas = res.fetchall()
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    for row in mas:
        team_id = row[2]
        if team_id not in dict_team:
            dict_team[team_id] = len(dict_team)
        team = team_a if dict_team[team_id] == 0 else team_b
        team.append({'name': row[0], 'id': row[1], 'team_name': row[2], 'arrival': row[3], 'team_id': row[4]})
    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


@router.get('/api/total_points_stud_for_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Group comparison page"], description=
            """
                    Получает id_team1: int, id_team2: int
                    Returns:
                        [{'name': row[0], 'id': row[1], 'team_name': row[2], 'total_points': row[3], 'team_id': row[4]},...]
                    \n
                    [
                      {
                        "name": "1d2e6ef2292169073155afe2f7b4b27d158f4b0f1642911ab52ac88258505e8a",
                        "id": 185,
                        "team_name": "ПиОА П-08.02",
                        "total_points": 96.93,
                        "team_id": 2
                      },
                      {
                        "name": "7d2e36f95f2530714b85f21a08c5c4bf6b8c59f6fbdc50ce1b22efac5a7e521f",
                        "id": 300,
                        "team_name": "ПиОА П-04.03",
                        "total_points": 95.97,
                        "team_id": 4
                      },
                      {
                        "name": "809735612a2046a206b1d11a71013781f00835befef1318d5cfb8568398686b7",
                        "id": 709,
                        "team_name": "ПиОА П-08.02",
                        "total_points": 92.61,
                        "team_id": 2
                      },
                      {
                        "name": "107183af1dc1bb923b4f7163d8e0de1af69f3da43b9797eec9db66727f51f854",
                        "id": 289,
                        "team_name": "ПиОА П-04.03",
                        "total_points": 94.06,
                        "team_id": 4
                      },
            """)
async def total_points_stud_for_teams(id_team1: int, id_team2: int, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    res = await db.execute(f"""
            SELECT DISTINCT
                (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS name,
                (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS id,
                (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
                ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id) + SUM(l.test) OVER (PARTITION BY stud_id))::DECIMAL, 2) AS cum_sum,
                (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id
            FROM
                lesson l
            WHERE
                l.team_id = {id_team1} OR l.team_id = {id_team2}
            order by cum_sum desc
        """)
    mas = res.fetchall()
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    for row in mas:
        team_id = row[2]
        if team_id not in dict_team:
            dict_team[team_id] = len(dict_team)
        team = team_a if dict_team[team_id] == 0 else team_b
        team.append({'name': row[0], 'id': row[1], 'team_name': row[2], 'total_points': row[3], 'team_id': row[4]})
    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


@router.get('/api/attendance_static_stud_for_all_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Group comparison page"], description=
            """
                    Получает token: str
                    Returns:
                        [{'team_name': row[0], 'arrival': row[1], 'team_id': row[2], 'teacher_id': row[3], 'teacher_name': row[4]},...]
                    \n
                    [
                      {
                        "team_name": "ПиОА Л-08",
                        "arrival": 68.51851851851852,
                        "team_id": 1,
                        "teacher_id": 1,
                        "teacher_name": "Плотоненко Юрий Анатольевич"
                      },
                      {
                        "team_name": "ПиОА П-08.02",
                        "arrival": 77.87878787878788,
                        "team_id": 2,
                        "teacher_id": 2,
                        "teacher_name": "Трефилин Иван Андреевич"
                      },
            """)
async def attendance_static_stud_for_all_teams(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    res = await db.execute(f"""
        SELECT distinct
            (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
            ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.team_id) / COUNT(id) OVER (PARTITION BY l.team_id)::DECIMAL, 2) AS arrival,
            (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id,
            (SELECT t.id FROM teacher t WHERE t.id = l.teacher_id) AS teacher_id,
            (SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_name
        FROM
            lesson l
        where
            l.team_id in ({teams_true})
        order by arrival desc
    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/total_points_studs_for_all_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Group comparison page"], description=
            """
                    Получает token: str
                    Returns:
                        [{'team_name': row[0], 'avg_total_points': row[1], 'team_id': row[2], 'teacher_id': row[3], 'teacher_name': row[4]},...]
                    \n
                    [
                      {
                        "team_name": "ПиОА Л-08",
                        "avg_total_points": 0,
                        "team_id": 1,
                        "teacher_id": 1,
                        "teacher_name": "Плотоненко Юрий Анатольевич"
                      },
                      {
                        "team_name": "ПиОА П-08.02",
                        "avg_total_points": 67.72099666666666,
                        "team_id": 2,
                        "teacher_id": 2,
                        "teacher_name": "Трефилин Иван Андреевич"
                      },
            """)
async def total_points_studs_for_all_teams(token: str, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    res = await db.execute(f"""
        SELECT
            (SELECT t.name FROM team t WHERE t.id = l.team_id) AS team_name,
            ROUND(((SUM(l.mark_for_work) + SUM(l.test))/COUNT(DISTINCT stud_id))::DECIMAL, 2) AS avg_total_points,
            (SELECT t.id FROM team t WHERE t.id = l.team_id) AS team_id,
            (SELECT t.id FROM teacher t WHERE t.id = l.teacher_id) AS teacher_id,
            (SELECT t.name FROM teacher t WHERE t.id = l.teacher_id) AS teacher_name
        FROM
            lesson l
        WHERE
            l.team_id IN ({teams_true})
        GROUP BY
            team_id, teacher_id, teacher_name, team_name
        ORDER BY
            avg_total_points DESC;
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/team_kr_total_points_attendance_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Group comparison page"], description=
            """
                    Получает token: str, group_by_teacher, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")
                    
                    [
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм", название команды
                        "team_id": 35, айди команды
                        "teacher_id": 4, айди преподавателя
                        "teacher_name": "Павлова Елена Александровна", название преподавателя
                        "Успеваемость_средняя": 31.77, средняя успеваемость команды на определенном майлстоуне
                        "Посещаемость_средняя": 0.94 средняя посещаемость команды на определенном майлстоуне
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Успеваемость_средняя": 53.28,
                        "Посещаемость_средняя": 0.94
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Успеваемость_средняя": 84.11,
                        "Посещаемость_средняя": 0.93
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Успеваемость_средняя": 86.43,
                        "Посещаемость_средняя": 0.89
                      },
            """)
async def team_kr_total_points_attendance_dynamic(token: str, group_by_teacher: bool,
                                                  teacher_list: Optional[str] = None,
                                                  db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    if group_by_teacher:
        fields = """"""
        partition_by = "sub.name, sub.teacher_id"
    else:
        fields = """sub.team_name,
                    sub.team_id,"""
        partition_by = "sub.name, sub.teacher_id, sub.team_id"
    res = await db.execute(f"""
        SELECT DISTINCT
            {fields}
            sub.teacher_id,
            sub.teacher_name,
            ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя,
            ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Посещаемость_средняя
        FROM
            (
                SELECT
                    (
                        SELECT t.name FROM team t WHERE t.id = l.team_id
                    ) AS team_name,
                    ROUND(
                        (
                            SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                            SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                        )::DECIMAL,
                        2
                    ) AS Успеваемость,
                    ROUND(
                        COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                        COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
                        2
                    ) AS dynamical_arrival,
                    (
                        SELECT t.id FROM team t WHERE t.id = l.team_id
                    ) AS team_id,
                    (
                        SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_id,
                    (
                        SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_name,
                    l.name
                FROM
                    lesson l
                WHERE
                    l.team_id IN ({teams_true})
            ) AS sub
        WHERE
            sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/team_kr_total_points_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Group comparison page"], description=
            """
                    Получает token: str, group_by_teacher, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")
                    
                    [
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм", название команды
                        "team_id": 35, айди команды
                        "teacher_id": 4, айди преподавателя
                        "teacher_name": "Павлова Елена Александровна", название преподавателя
                        "Успеваемость_средняя": 31.77 средняя успеваемость команды на определенном майлстоуне
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Успеваемость_средняя": 53.28
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Успеваемость_средняя": 84.11
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Успеваемость_средняя": 86.43
                      },
            """)
async def team_kr_total_points_dynamic(token: str, group_by_teacher: bool,
                                       teacher_list: Optional[str] = None,
                                       db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    if group_by_teacher:
        fields = """"""
        partition_by = "sub.name, sub.teacher_id"
    else:
        fields = """sub.team_name,
                    sub.team_id,"""
        partition_by = "sub.name, sub.teacher_id, sub.team_id"
    res = await db.execute(f"""
        SELECT DISTINCT
            {fields}
            sub.teacher_id,
            sub.teacher_name,
            ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя
        FROM
            (
                SELECT
                    (
                        SELECT t.name FROM team t WHERE t.id = l.team_id
                    ) AS team_name,
                    ROUND(
                        (
                            SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                            SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                        )::DECIMAL,
                        2
                    ) AS Успеваемость,
                    (
                        SELECT t.id FROM team t WHERE t.id = l.team_id
                    ) AS team_id,
                    (
                        SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_id,
                    (
                        SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_name,
                    l.name
                FROM
                    lesson l
                WHERE
                    l.team_id IN ({teams_true})
            ) AS sub
        WHERE
            sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/team_kr_attendance_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Group comparison page"], description=
            """
                    Получает token: str, group_by_teacher, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")
                    
                    [
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм", название команды
                        "team_id": 35, айди команды
                        "teacher_id": 4, айди преподавателя
                        "teacher_name": "Павлова Елена Александровна", название преподавателя
                        "Посещаемость_средняя": 0.94 средняя посещаемость команды на определенном майлстоуне
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Посещаемость_средняя": 0.94
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Посещаемость_средняя": 0.93
                      },
                      {
                        "team_name": "ПиОА П-01.01 Спорт Прогрм",
                        "team_id": 35,
                        "teacher_id": 4,
                        "teacher_name": "Павлова Елена Александровна",
                        "Посещаемость_средняя": 0.89
                      },
            """)
async def team_kr_attendance_dynamic(token: str, group_by_teacher: bool,
                                     teacher_list: Optional[str] = None,
                                     db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    if group_by_teacher:
        fields = """"""
        partition_by = "sub.name, sub.teacher_id"
    else:
        fields = """sub.team_name,
                    sub.team_id,"""
        partition_by = "sub.name, sub.teacher_id, sub.team_id"
    res = await db.execute(f"""
        SELECT DISTINCT
            {fields}
            sub.teacher_id,
            sub.teacher_name,
            ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Посещаемость_средняя
        FROM
            (
                SELECT
                    (
                        SELECT t.name FROM team t WHERE t.id = l.team_id
                    ) AS team_name,
                    ROUND(
                        COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                        COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
                        2
                    ) AS dynamical_arrival,
                    (
                        SELECT t.id FROM team t WHERE t.id = l.team_id
                    ) AS team_id,
                    (
                        SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_id,
                    (
                        SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_name,
                    l.name
                FROM
                    lesson l
                WHERE
                    l.team_id IN ({teams_true})
            ) AS sub
        WHERE
            sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


# endregion

# Speciality comparison page
# region
@router.get('/api/attendance_static_for_specialities', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, speciality1: str, speciality2: str, lect: bool,
                    Returns:
                        [{'arrival': row[0], 'speciality': row[1], 'id': row[2]},...]
                    \n
                    [
                      {
                        "arrival": 100,
                        "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
                        "id": 2
                      },
                      {
                        "arrival": 96.42857142857143,
                        "speciality": "01.03.03 Механика и математическое моделирование",
                        "id": 67
                      },
            """)
async def attendance_static_for_specialities(token: str, speciality1: str, speciality2: str, lect: bool,
                                             db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    res = await db.execute(f"""
        SELECT DISTINCT
            ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id) / COUNT(l.id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS arrival,
            s.speciality AS speciality,
            s.id AS id
        FROM
            lesson l
        inner join stud s on s.id = l.stud_id
        WHERE
            l.team_id IN ({teams_true})
            and (s.speciality = '{speciality1}' or s.speciality = '{speciality2}')
        order by arrival desc
        """)
    mas = res.fetchall()
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    for row in mas:
        team_id = row[1]
        if team_id not in dict_team:
            dict_team[team_id] = len(dict_team)
        team = team_a if dict_team[team_id] == 0 else team_b
        team.append({'arrival': row[0], 'speciality': row[1], 'id': row[2]})
    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


@router.get('/api/total_points_for_specialities', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, speciality1: str, speciality2: str, lect: bool,
                    Returns:
                        [{'total_points': row[0], 'speciality': row[1], 'id': row[2]},...]
                    \n
                    [
                      {
                        "total_points": 93.21,
                        "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
                        "id": 727
                      },
                      {
                        "total_points": 91.3,
                        "speciality": "01.03.03 Механика и математическое моделирование",
                        "id": 387
                      },
                      {
                        "total_points": 91.8,
                        "speciality": "10.05.03 Информационная безопасность автоматизированных систем",
                        "id": 192
                      },
            """)
async def total_points_for_specialities(token: str, speciality1: str, speciality2: str, lect: bool,
                                        db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    res = await db.execute(f"""
            SELECT DISTINCT
                ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id) + SUM(l.test) OVER (PARTITION BY stud_id))::DECIMAL, 2) AS total_points,
                s.speciality AS speciality,
                s.id AS id
            FROM
                lesson l
            inner join stud s on s.id = l.stud_id
            WHERE
                l.team_id IN ({teams_true})
                and (s.speciality = '{speciality1}' or s.speciality = '{speciality2}')
            order by arrival desc
            """)
    mas = res.fetchall()
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    for row in mas:
        team_id = row[1]
        if team_id not in dict_team:
            dict_team[team_id] = len(dict_team)
        team = team_a if dict_team[team_id] == 0 else team_b
        team.append({'total_points': row[0] if row[0] > 0 else 0, 'speciality': row[1], 'id': row[2]})
    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


@router.get('/api/attendance_static_stud_for_all_specialities', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, lect: bool,
                    Returns:
                        [{'arrival': row[0], 'Stud_speciality': row[1], 'studs_in_speciality': row[2]},...]
                    \n
                    [
                      {
                        "arrival": 67.85714285714286,
                        "Stud_speciality": "01.03.01 Математика",
                        "studs_in_speciality": 22
                      },
                      {
                        "arrival": 75.31055900621118,
                        "Stud_speciality": "01.03.03 Механика и математическое моделирование",
                        "studs_in_speciality": 23
                      },
            """)
async def attendance_static_stud_for_all_specialities(token: str, lect: bool,
                                                      db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    res = await db.execute(f"""
        SELECT
            ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') / COUNT(l.id)::DECIMAL, 2) AS arrival,
            s.speciality AS Stud_speciality,
            count(distinct s.id) AS studs_in_speciality
        FROM
            lesson l
        inner join stud s on s.id = l.stud_id
        WHERE
            l.team_id IN ({teams_true})
        group by s.speciality 
        order by arrival desc
                """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/total_points_studs_for_all_specialities', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, lect: bool,
                    Returns:
                        [{'Stud_speciality': row[0], 'avg_total_points': row[2] / row[1], 'studs_in_speciality': row[1]},...]
                    \n
                    [
                      {
                        "Stud_speciality": "01.03.01 Математика",
                        "avg_total_points": 42.32272727272727,
                        "studs_in_speciality": 22
                      },
                      {
                        "Stud_speciality": "01.03.03 Механика и математическое моделирование",
                        "avg_total_points": 56.73652608695652,
                        "studs_in_speciality": 23
                      },
            """)
async def total_points_studs_for_all_specialities(token: str, lect: bool, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    res = await db.execute(f"""
            select
                s.speciality AS Stud_speciality,
                ROUND(((SUM(l.mark_for_work) + SUM(l.test))/COUNT(DISTINCT stud_id))::DECIMAL, 2) AS avg_total_points,
                count(distinct s.id) AS studs_in_speciality
            FROM
                lesson l
            inner join stud s on s.id = l.stud_id
            WHERE
                l.team_id IN ({teams_true})
            group by s.speciality 
            order by avg_total_points desc
    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/attendance_static_total_points_studs_for_all_specialities', name='Plot:plot',
            status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, lect: bool,
                    Returns:
                        [{'Stud_speciality': row[0], 'avg_total_points': row[2] / row[1], 'studs_in_speciality': row[1]},...]
                    \n
                    [
                      {
                        "Stud_speciality": "01.03.01 Математика",
                        "avg_total_points": 42.32272727272727,
                        "studs_in_speciality": 22
                      },
                      {
                        "Stud_speciality": "01.03.03 Механика и математическое моделирование",
                        "avg_total_points": 56.73652608695652,
                        "studs_in_speciality": 23
                      },
            """)
async def all_for_studs_for_all_specialities(token: str, lect: bool, db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    res = await db.execute(f"""
            select
                s.speciality AS Stud_speciality,
                ROUND(((SUM(l.mark_for_work) + SUM(l.test))/COUNT(DISTINCT stud_id))::DECIMAL, 2) AS avg_total_points,
                ROUND(COUNT(l.id) FILTER (WHERE l.arrival = 'П') / COUNT(l.id)::DECIMAL, 2) AS arrival,
                count(distinct s.id) AS studs_in_speciality
            FROM
                lesson l
            inner join stud s on s.id = l.stud_id
            WHERE
                l.team_id IN ({teams_true})
            group by s.speciality 
            order by avg_total_points desc
    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/speciality_kr_total_points_attendance_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, group_by_speciality, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                    [
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем", направление
                        "teacher_name": "Плотоненко Юрий Анатольевич", ФИО преподавателя
                        "teacher_id": 1, айди преподавателя
                        "Успеваемость_средняя": 18.83,  средняя успеваемость команды на определенном майлстоуне
                        "Посещаемость_средняя": 0.52 средняя посещаемость команды на определенном майлстоуне
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Успеваемость_средняя": 35.5,
                        "Посещаемость_средняя": 0.51
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Успеваемость_средняя": 50.5,
                        "Посещаемость_средняя": 0.53
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Успеваемость_средняя": 53.33,
                        "Посещаемость_средняя": 0.52
                      },
            """)
async def speciality_kr_total_points_attendance_dynamic(token: str, group_by_speciality: bool,
                                                        teacher_list: Optional[str] = None,
                                                        db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    if group_by_speciality:
        fields = """"""
        partition_by = "sub.Stud_speciality, sub.name"
    else:
        fields = """sub.teacher_name,
                    sub.teacher_id,"""
        partition_by = "sub.Stud_speciality, sub.name, sub.teacher_id"
    res = await db.execute(f"""
        SELECT DISTINCT
            sub.Stud_speciality,
            {fields}
            ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя,
            ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Посещаемость_средняя
        FROM
            (
                SELECT
                    s.speciality AS Stud_speciality,
                    ROUND(
                        (
                            SUM(l.mark_for_work) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                            SUM(l.test) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                        )::DECIMAL,
                        2
                    ) AS Успеваемость,
                    ROUND(
                        COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                        COUNT(l.id) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
                        2
                    ) AS dynamical_arrival,
                    (
                        SELECT t.id FROM team t WHERE t.id = l.team_id
                    ) AS team_id,
                    (
                        SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_id,
                    (
                        SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_name,
                    l.name
                FROM
                    lesson l
                INNER JOIN stud s ON s.id = l.stud_id
                WHERE
                    l.team_id IN ({teams_true})
            ) AS sub
        WHERE 
            sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/speciality_kr_attendance_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, group_by_speciality, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                    [
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем", направление
                        "teacher_name": "Плотоненко Юрий Анатольевич", ФИО преподавателя
                        "teacher_id": 1, айди преподавателя
                        "Посещаемость_средняя": 0.52 средняя посещаемость команды на определенном майлстоуне
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Посещаемость_средняя": 0.51
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Посещаемость_средняя": 0.53
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Посещаемость_средняя": 0.52
                      },
            """)
async def speciality_kr_attendance_dynamic(token: str, group_by_speciality: bool,
                                           teacher_list: Optional[str] = None,
                                           db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    if group_by_speciality:
        fields = """"""
        partition_by = "sub.Stud_speciality, sub.name"
    else:
        fields = """sub.teacher_name,
                    sub.teacher_id,"""
        partition_by = "sub.Stud_speciality, sub.name, sub.teacher_id"
    res = await db.execute(f"""
        SELECT DISTINCT
            sub.Stud_speciality,
            {fields}
            ROUND(AVG(sub.dynamical_arrival) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Посещаемость_средняя
        FROM
            (
                SELECT
                    s.speciality AS Stud_speciality,
                    ROUND(
                        COUNT(l.id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) / 
                        COUNT(l.id) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL,
                        2
                    ) AS dynamical_arrival,
                    (
                        SELECT t.id FROM team t WHERE t.id = l.team_id
                    ) AS team_id,
                    (
                        SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_id,
                    (
                        SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_name,
                    l.name
                FROM
                    lesson l
                INNER JOIN stud s ON s.id = l.stud_id
                WHERE
                    l.team_id IN ({teams_true})
            ) AS sub
        WHERE 
            sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/speciality_kr_total_points_dynamic', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Speciality comparison page"], description=
            """
                    Получает token: str, group_by_speciality, teacher_list (пример "Павлова Елена Александровна,Павлова Елена Александровна")

                    [
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем", направление
                        "teacher_name": "Плотоненко Юрий Анатольевич", ФИО преподавателя
                        "teacher_id": 1, айди преподавателя
                        "Успеваемость_средняя": 18.83  средняя успеваемость команды на определенном майлстоуне
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Успеваемость_средняя": 35.5
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Успеваемость_средняя": 50.5
                      },
                      {
                        "stud_speciality": "02.03.03 Математическое обеспечение и администрирование информационных систем",
                        "teacher_name": "Плотоненко Юрий Анатольевич",
                        "teacher_id": 1,
                        "Успеваемость_средняя": 53.33
                      },
            """)
async def speciality_kr_total_points_dynamic(token: str, group_by_speciality: bool,
                                             teacher_list: Optional[str] = None,
                                             db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    if teacher_list is not None:
        teacher_arr = teacher_list.split(',')
        teams = await get_teams_for_param_private_without_lect(teacher_arr=teacher_arr, db=db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    if group_by_speciality:
        fields = """"""
        partition_by = "sub.Stud_speciality, sub.name"
    else:
        fields = """sub.teacher_name,
                    sub.teacher_id,"""
        partition_by = "sub.Stud_speciality, sub.name, sub.teacher_id"
    res = await db.execute(f"""
        SELECT DISTINCT
            sub.Stud_speciality,
            {fields}
            ROUND(AVG(sub.Успеваемость) OVER (PARTITION BY {partition_by})::DECIMAL, 2) AS Успеваемость_средняя
        FROM
            (
                SELECT
                    s.speciality AS Stud_speciality,
                    ROUND(
                        (
                            SUM(l.mark_for_work) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) +
                            SUM(l.test) OVER (PARTITION BY l.stud_id, s.speciality ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
                        )::DECIMAL,
                        2
                    ) AS Успеваемость,
                    (
                        SELECT t.id FROM team t WHERE t.id = l.team_id
                    ) AS team_id,
                    (
                        SELECT t.id FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_id,
                    (
                        SELECT t.name FROM teacher t WHERE t.id = l.teacher_id
                    ) AS teacher_name,
                    l.name
                FROM
                    lesson l
                INNER JOIN stud s ON s.id = l.stud_id
                WHERE
                    l.team_id IN ({teams_true})
            ) AS sub
        WHERE 
            sub.name IN ('Организация функций30', 'Коллекции. Работа с файлами20', 'Управляющие конструкции50', 'Аттестация00');
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


# endregion

# kr page
# region
@router.get('/api/kr_analyse_simple', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["kr page"], description=
            """
                    Получает token: str, type: int, kr: str,
                    Returns:
                        Словарь с ключами(преподаватели/аправления/команды)
                    \n
                    {
                      "Трефилин Иван Андреевич": [
                        12,
                        0,
                        14.43,
                        3,
                        6.83,
                        12.3,
                        2,
            """)
async def kr_analyse_simple(token: str, type_group_by: int, kr: str,
                            db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = ', '.join([f"'{team[0]}'" for team in teams])
    match type_group_by:
        case 0:
            fill_query_str = '(select t.name from team t where t.id = l.team_id)'
            fill_query_str2 = 'group by l.team_id'
        case 1:
            fill_query_str = '(select s.speciality from stud s where s.id = l.stud_id) as speciality'
            fill_query_str2 = 'group by speciality'
        case 2:
            fill_query_str = '(select t.name from teacher t where t.id = l.teacher_id) as teacher_name'
            fill_query_str2 = 'group by teacher_name'
        case _:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Неправильно выбран тип 0 - Группировка по командам, 1 - " +
                                       "Группировка по направлениям, 2 - Группировка по преподавателям")
    res = await db.execute(f"""
        SELECT
            ARRAY_AGG(l.test) AS test_mark_list,
            {fill_query_str}
        FROM
            lesson l
        WHERE
            l.team_id IN ({teams_true})
            and l.name = '{kr}'
        {fill_query_str2}
    """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


@router.get('/api/kr_analyse_with_filters', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["kr page"], description=
            """
                    Получает token: str, kr: str, type:int, teacher: Optional[str] = None, speciality: Optional[str] = None,
                                  team: Optional[str] = None,
                    Returns:
                        Словарь с ключами(преподаватели/аправления/команды) и любые их сочетания(проверь чтоб понять)
                    \n
                    {
                      "Трефилин Иван Андреевич": [
                        12,
                        0,
                        14.43,
                        3,
                        6.83,
                        12.3,
                        2,
            """)
async def kr_analyse_with_filters(token: str, kr: str, type_select: int, teacher: Optional[str] = None,
                                  speciality: Optional[str] = None, team: Optional[str] = None,
                                  db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    if teacher is None:
        teachers = await get_all_teachers(token, db)
        teachers = ', '.join([f"'{teacher[0]}'" for teacher in teachers])
    else:
        teachers = teacher
    if speciality is None:
        specialities = await get_all_specialities(token, db)
        specialities = ', '.join([f"'{speciality[0]}'" for speciality in specialities])
    else:
        specialities = speciality
    if team is None:
        teams = await get_teams_for_user_private_without_lect(token, db)
        teams = ', '.join([f"'{team[0]}'" for team in teams])
    else:
        teams = team
    team_query = ''
    teacher_query = ''
    speciality_query = ''
    match type_select:
        case 0:
            team_query = 't1.name as team_name'
            group_by_query = 'group by team_name'
        case 1:
            teacher_query = 't.name as teacher_name'
            group_by_query = 'group by teacher_name'
        case 2:
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality'
        case 3:
            team_query = 't1.name as team_name'
            teacher_query = 't.name as teacher_name,'
            group_by_query = 'group by teacher_name,team_name'
        case 4:
            team_query = 't1.name as team_name,'
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality,team_name'
        case 5:
            teacher_query = 't.name as teacher_name,'
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality,teacher_name'
        case 6:
            team_query = 't1.name as team_name,'
            teacher_query = 't.name as teacher_name,'
            speciality_query = 's.speciality as speciality'
            group_by_query = 'group by speciality,teacher_name,team_name'
        case _:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Неправильно выбран тип(всего их 0,1,2,3,4,5,6)")
    res = await db.execute(f"""
        SELECT
            ARRAY_AGG(l.test) AS test_mark_list,
            {teacher_query}
            {team_query}
            {speciality_query}
        FROM
            lesson l
        inner join teacher t on t.id = l.teacher_id
        inner join team t1 on t1.id = l.team_id
        inner join stud s on s.id = l.stud_id
        WHERE
            l.name = '{kr}'
            and l.team_id IN ({teams})
            and t.id IN ({teachers})
            and s.speciality IN ({specialities})
        {group_by_query}
        """)
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return res.fetchall()


# endregion

# query builder page
# region


@router.post('/api/get_dataset', name='Reporting system:Reporting system', status_code=status.HTTP_200_OK,
             tags=["Reporting system page"], description=
             """
                     Получает fields_dict: dict | None, filter_dict: dict | None, distinct: bool,
                     рабочие параметры fields_dict снизу
                     field_params = ['lesson_id', 'lesson_name', 'lesson_mark_for_work', 'lesson_arrival', 'lesson_test',
                     'lesson_result_points', 'lesson_result_mark', 'lesson_stud_id', 'lesson_team_id',
                     'lesson_teacher_id', 'lesson_date_of_add', 'rmup_id', 'rmup_name', 'rmup_link', 'rmup_date_of_add',
                     'stud_id', 'stud_name', 'stud_email', 'stud_speciality', 'stud_date_of_add', 'teacher_id',
                     'teacher_name', 'teacher_lect_or_pract', 'teacher_date_of_add', 'team_id',
                     'team_name', 'team_rmup_id', 'team_date_of_add']
                     рабочие параметры filter_dict это строка команд/учителей/направлений разреденных символом '_'
                     filter_dict_true = {'teams':"","teachers":"Плотоненко Юрий Анатольевич_Трефилин Иван Андреевич","specialities":""}
                     Returns:
                         грубо говоря ссылку на скачивание csv файла
             """)
async def get_dataset(fields_dict: dict | None, filter_dict: dict | None, distinct: bool,
                      db: AsyncSession = Depends(connect_db_data)):
    start_time = time.time()
    print(fields_dict)
    # field_params = ['lesson_id', 'lesson_name', 'lesson_mark_for_work', 'lesson_arrival', 'lesson_test',
    #                 'lesson_result_points', 'lesson_result_mark', 'lesson_stud_id', 'lesson_team_id',
    #                 'lesson_teacher_id', 'lesson_date_of_add', 'rmup_id', 'rmup_name', 'rmup_link', 'rmup_date_of_add',
    #                 'stud_id', 'stud_name', 'stud_email', 'stud_speciality', 'stud_date_of_add', 'teacher_id',
    #                 'teacher_name', 'teacher_lect_or_pract', 'teacher_date_of_add', 'team_id',
    #                 'team_name', 'team_rmup_id', 'team_date_of_add']
    field_dict_true = {'lesson_id': "l.id", 'lesson_name': "l.name",
                       'lesson_mark_for_work': "l.mark_for_work", 'lesson_arrival': "l.arrival",
                       'lesson_test': "l.test", 'lesson_result_points': "l.result_points",
                       'lesson_result_mark': "l.result_mark",
                       'lesson_stud_id': "l.stud_id", 'lesson_team_id': "l.team_id",
                       'lesson_teacher_id': "l.teacher_id",
                       'lesson_date_of_add': "l.date_of_add", 'rmup_id': "r.id", 'rmup_name': "r.name",
                       'rmup_link': "r.link", 'rmup_date_of_add': "r.date_of_add", 'stud_id': "s.id",
                       'stud_name': "s.name", 'stud_email': "s.email", 'stud_speciality': "s.speciality",
                       'stud_date_of_add': "s.date_of_add", 'teacher_id': "t.id",
                       'teacher_name': "t.name",
                       'teacher_lect_or_pract': "t.lect_or_pract", 'teacher_date_of_add': "t.date_of_add",
                       'team_id': "t2.id", 'team_name': "t2.name", 'team_rmup_id': "t2.rmup_id",
                       'team_date_of_add': "t2.date_of_add"}
    # filter_dict_true = {'teams':"","teachers":"Плотоненко Юрий Анатольевич_Трефилин Иван Андреевич","specialities":""}
    # filter_dict = filter_dict_true
    if len(filter_dict) > 0:
        teams_str = ''
        teachers_str = ''
        specialities_str = ''
        if filter_dict['teams'] != "":
            teams = filter_dict['teams'].split("_")
            teams = ', '.join([f"'{team}'" for team in teams])
            teams_str = f'and t2.name IN ({teams})'
        if filter_dict['teachers'] != "":
            teachers = filter_dict['teachers'].split("_")
            teachers = ', '.join([f"'{teacher}'" for teacher in teachers])
            teachers_str = f'and t.name IN ({teachers})'
        if filter_dict['specialities'] != "":
            specialities = filter_dict['specialities'].split("_")
            specialities = ', '.join([f"'{speciality}'" for speciality in specialities])
            specialities_str = f'and s.speciality IN ({specialities})'
        filter_str = f'where 1=1 {teams_str}{teachers_str}{specialities_str}'
    else:
        filter_str = ''
    field_list_str = ''
    if fields_dict is not None:
        for key, value in fields_dict.items():
            field_list_str += field_dict_true[str(value)] + ','
        field_list_str = field_list_str[:-1]
    else:
        field_list_str = '*'
    if field_list_str == '':
        field_list_str = '*'
    if distinct:
        distinct_str = ' distinct '
    else:
        distinct_str = ''
    result_query = await db.execute(f"""
        SELECT {distinct_str}
            {field_list_str}
        from lesson l
        inner join teacher t on t.id = l.teacher_id 
        inner join team t2 on t2.id  = l.team_id 
        inner join stud s on s.id = l.stud_id
        inner join rmup r on r.id = t2.rmup_id
        {filter_str}
                    """)
    df = pd.DataFrame(result_query.fetchall())
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                 )
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    return response


@router.post('/api/reporting_system', name='Reporting system:Reporting system', status_code=status.HTTP_200_OK,
             tags=["Reporting system page"], description=
             """
                     Получает hrefs_list: str, name_of_sheet_list: str, as_csv: bool
                     hrefs_list это, к примеру, http://localhost:8090/api/cum_sum_points_for_stud_for_team?id_team=2&id_stud=1,http://localhost:8090/api/cum_sum_points_for_stud_for_team?id_team=2&id_stud=1
                     name_of_sheet_list такая же строка с разделителем ',', которая называет страницы csv
                     Returns:
                         массив словарей с полями 'response', "url" либо ссылку на скачивает csv файла
             """)
async def reporting_system(hrefs_list: str, name_of_sheet_list: str, as_csv: bool):
    hrefs_list = hrefs_list.split(',')
    name_of_sheet_list = name_of_sheet_list.split(',')
    res = await get_urls(hrefs_list, as_csv)
    if isinstance(res, dict):
        res = [res]
    if as_csv:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
        file_path = f"trash/{random_string}.xlsx"
        writer = pd.ExcelWriter(file_path, engine="xlsxwriter")
        for index, href_resp in enumerate(res, start=0):
            df = pd.DataFrame(href_resp)
            df.to_excel(writer, sheet_name=f"{name_of_sheet_list[index]}", index=False)
        writer.close()
        with open(file_path, "rb") as file:
            contents = file.read()
        response = StreamingResponse(iter([contents]),
                                     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["Content-Disposition"] = "attachment; filename=export.xlsx"
        os.remove(file_path)
        return response
    else:
        return res

# endregion
