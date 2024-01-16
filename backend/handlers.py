import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional

import matplotlib.pyplot as plt
import jwt
import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import func, Float
from sqlalchemy.sql.expression import and_, case, cast, or_, distinct
from starlette import status
from starlette.exceptions import HTTPException

from models import connect_db_data, connect_db_users, Lesson, Team, User, Stud, Teacher
from schemas import UserRegistration, TokenData, UserLogin
from util import Hasher

router = APIRouter()

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
                         Если юзер есть, то  raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Пользователь с такими данными уже существует(юзернейм, емейл)")
 
                     Returns:
                         {"access_token": access_token, "token_type": "bearer"}
                    \n
                    {
                      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJGSU8iOiJzdHJpbmciLCJpc0FkbWluIjp0cnVlLCJpc0N1cmF0b3IiOnRydWUsImlzVGVhY2hlciI6dHJ1ZSwidXNlcm5hbWUiOiJzdHJpbmciLCJwYXNzd29yZCI6InN0cmluZyIsImVtYWlsIjoic3RyaW5nIiwiZXhwIjoxNzA1MDcwNzU5fQ.WZShrhvSyHaGFvEumrcQh86CVg3m4wa7O_-tfmlhXNI",
                      "token_type": "bearer"
                    }
             """)
async def registration_standard(user: UserRegistration, db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    checkuser = db.query(User).filter(and_(User.username == user.username, User.email == user.email)).first()
    if checkuser is not None:
        db.close()
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
    db.commit()
    db.close()
    print({"access_token": access_token, "token_type": "bearer"})
    return {"access_token": access_token, "token_type": "bearer"}


def get_user(username, email):
    db = connect_db_users()
    res = db.query(User).filter(and_(User.username == username, User.email == email)).first()
    db.close()
    return res


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
        print(payload)
        username: str = payload.get("username")
        password: str = payload.get("password")
        email: str = payload.get("email")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, password=password, email=email)
        print(token_data)
    except:
        raise credentials_exception
    user = get_user(username=token_data.username, email=token_data.email)
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
async def get_all_users(db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    all_users = db.query(User).all()
    return all_users


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
async def delete_all_users(db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    db.query(User).delete()
    db.commit()
    return {"message": "All users deleted successfully"}


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
async def login_standard(user: UserLogin, db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    checkuser = db.query(User).filter(and_(User.username == user.username, User.email == user.email)).first()
    print(checkuser)
    if checkuser is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Нельзя войти в несуществующий аккаунт/Неправильно введены данные")
    is_true_login = Hasher.verify_password(user.password, checkuser.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"FIO": checkuser.fio, "isAdmin": checkuser.isadmin, "isCurator": checkuser.iscurator,
              "isTeacher": checkuser.isteacher,
              "username": checkuser.username, "password": checkuser.password, "email": checkuser.email},
        expires_delta=access_token_expires
    )
    db.close()
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
async def get_teams_for_user(token: str, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = db.query(Team.id, Team.name).distinct().all()
        db.close()
        return response
    elif user.isteacher:
        # todo вот эту строчку поменять шо она будет искать подстроку user_fio в Teacher.name
        teacher_id_query = db.query(Teacher.id).filter(Teacher.name.like(f"%{user_fio}%")).all()
        teacher_id_list = [row[0] for row in teacher_id_query]
        team_id_query = db.query(Lesson.team_id).filter(Lesson.teacher_id.in_(teacher_id_list)).distinct().all()
        team_id_list = [row[0] for row in team_id_query]
        response = db.query(Team.id, Team.name).filter(Team.id.in_(team_id_list)).distinct().all()
        db.close()
        return response
    else:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


async def get_teams_for_user_private(token: str, db):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = db.query(Team.id, Team.name).distinct().all()
        db.close()
        return response
    elif user.isteacher:
        # todo вот эту строчку поменять шо она будет искать подстроку user_fio в Teacher.name
        teacher_id_query = db.query(Teacher.id).filter(Teacher.name.like(f"%{user_fio}%")).all()
        teacher_id_list = [row[0] for row in teacher_id_query]
        team_id_query = db.query(Lesson.team_id).filter(Lesson.teacher_id.in_(teacher_id_list)).distinct().all()
        team_id_list = [row[0] for row in team_id_query]
        response = db.query(Team.id, Team.name).filter(Team.id.in_(team_id_list)).distinct().all()
        db.close()
        return response
    else:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


async def get_teams_for_user_private_without_lect(token: str, db):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = db.query(Team.id, Team.name).distinct().all()
        print(len(response))
        true_response = [item for item in response if 'Л' not in item[1]]
        print(len(true_response))
        db.close()
        return true_response
    elif user.isteacher:
        # todo вот эту строчку поменять шо она будет искать подстроку user_fio в Teacher.name
        teacher_id_query = db.query(Teacher.id).filter(Teacher.name.like(f"%{user_fio}%")).all()
        teacher_id_list = [row[0] for row in teacher_id_query]
        team_id_query = db.query(Lesson.team_id).filter(Lesson.teacher_id.in_(teacher_id_list)).distinct().all()
        team_id_list = [row[0] for row in team_id_query]
        response = db.query(Team.id, Team.name).filter(Team.id.in_(team_id_list)).distinct().all()
        true_response = [item for item in response if 'Л' not in item[1]]
        db.close()
        return true_response
    else:
        db.close()
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
async def get_teams_for_user_without_lect(token: str, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = db.query(Team.id, Team.name).distinct().all()
        print(len(response))
        true_response = [item for item in response if 'Л' not in item[1]]
        print(len(true_response))
        db.close()
        return true_response
    elif user.isteacher:
        # todo вот эту строчку поменять шо она будет искать подстроку user_fio в Teacher.name
        teacher_id_query = db.query(Teacher.id).filter(Teacher.name.like(f"%{user_fio}%")).all()
        teacher_id_list = [row[0] for row in teacher_id_query]
        team_id_query = db.query(Lesson.team_id).filter(Lesson.teacher_id.in_(teacher_id_list)).distinct().all()
        team_id_list = [row[0] for row in team_id_query]
        response = db.query(Team.id, Team.name).filter(Team.id.in_(team_id_list)).distinct().all()
        true_response = [item for item in response if 'Л' not in item[1]]
        db.close()
        return true_response
    else:
        db.close()
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
async def get_student(id_stud: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    all_users = db.query(Stud).filter(Stud.id == id_stud).first()
    return all_users


@router.get('/api/get_all_specialities', name='Stud:get_all_specialities', status_code=status.HTTP_200_OK,
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
async def get_all_specialities(token: str, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = db.query(Stud.speciality).distinct().all()
        db.close()
        print(len(response))
        return response
    elif user.isteacher:
        # todo вот эту строчку поменять шо она будет искать подстроку user_fio в Teacher.name
        teacher_id_query = db.query(Teacher.id).filter(Teacher.name.like(f"%{user_fio}%")).all()
        teacher_id_list = [row[0] for row in teacher_id_query]
        stud_id_query = db.query(Lesson.stud_id).filter(Lesson.teacher_id.in_(teacher_id_list)).distinct().all()
        stud_id_list = [row[0] for row in stud_id_query]
        response = db.query(Stud.speciality).filter(Stud.id.in_(stud_id_list)).distinct().all()
        print(len(response))
        db.close()
        return response
    else:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="ВАМ ЗАПРЕЩАЕТСЯ ВХОД В СЕКРЕТНЫЙ РАЗДЕЛ КОНТРОЛЯ УСПЕВАЕМОСТИ")


@router.get('/api/get_all_kr', name='Stud:get_all_kr', status_code=status.HTTP_200_OK, tags=["Util"], description=
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
async def get_all_kr(db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    all_users = db.query(Lesson.name).filter(Lesson.test >= 0.0).distinct().all()
    return all_users


@router.get('/api/get_all_teachers', name='Stud:get_all_teachers', status_code=status.HTTP_200_OK,
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
async def get_all_teachers(token: str, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    user = await get_current_user_dev(token)
    user_fio = user.fio
    if user.iscurator or user.isadmin:
        response = db.query(Teacher.id, Teacher.name).distinct().all()
        true_response = [item for item in response if ',' not in item[1]]
        db.close()
        return true_response
    elif user.isteacher:
        # todo вот эту строчку поменять шо она будет искать подстроку user_fio в Teacher.name
        teacher_id_query = db.query(Teacher.id, Teacher.name).filter(and_(Teacher.name.like(f"%{user_fio}%"))).all()
        true_response = [item for item in teacher_id_query if ',' not in item[1]]
        db.close()
        return true_response
    else:
        db.close()
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
async def attendance_per_stud_for_team(id_team: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    result_query = (
        db.query(
            Stud.name,
            Stud.id,
            (cast(func.count(case([(Lesson.arrival == 'П', 1)], else_=None)), Float) / func.count(
                Lesson.arrival)).label("Посещаемость"),
        )
            .filter(Lesson.team_id == id_team).join(Stud, Stud.id == Lesson.stud_id)
            .group_by(Stud.name, Stud.id)
            .all()
    )
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query


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
async def total_points_attendance_per_stud_for_team(id_team: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    result_query = (
        db.query(
            Stud.name,
            Stud.id,
            (func.sum(Lesson.mark_for_work) + func.sum(Lesson.test)).label("Успеваемость"),
            ((cast(func.count(case([(Lesson.arrival == 'П', 1)], else_=None)), Float) / func.count(
                Lesson.arrival)) * 100).label("Посещаемость"),

        )
            .filter(Lesson.team_id == id_team).join(Stud, Stud.id == Lesson.stud_id)
            .group_by(Stud.name, Stud.id)
            .all()
    )
    db.close()
    df_list = []
    total_points_sum = 0.0
    arrival_sum = 0.0
    for row in result_query:
        df_list.append({'Stud_name': row[0], 'Stud_id': row[1], 'Успеваемость': row[2] if row[2]>=0 else 0, 'Посещаемость': row[3]})
        total_points_sum += row[2]
        arrival_sum += row[3]
    df_list.append({'total_points_avg': total_points_sum / len(df_list), 'arrival_avg': arrival_sum / len(df_list)})
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    # print(result_query)
    # response_list = []
    # for row in result_query:
    #     response_list.append({
    #         "Итоговые баллы": row[0],
    #         "ФИО студента": row[1]})
    return df_list


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
async def total_points_per_stud_for_team(id_team: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    result_query = (
        db.query(
            Stud.name,
            Stud.id,
            (func.sum(Lesson.mark_for_work) + func.sum(Lesson.test)).label("Успеваемость")
        )
            .filter(Lesson.team_id == id_team).join(Stud, Stud.id == Lesson.stud_id)
            .group_by(Stud.name, Stud.id)
            .all()
    )
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return result_query


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
async def total_marks_for_team(id_team: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    result_query = (
        db.query(
            Stud.name,
            Stud.id,
            (func.sum(Lesson.mark_for_work) + func.sum(Lesson.test)).label("Успеваемость")
        )
            .filter(Lesson.team_id == id_team).join(Stud, Stud.id == Lesson.stud_id)
            .group_by(Stud.name, Stud.id)
            .all()
    )
    db.close()
    df_2 = []
    df_3 = []
    df_4 = []
    df_5 = []
    for row in result_query:
        if row[2] < 61:
            df_2.append({'Stud_name': row[0], 'Stud_id': row[1], 'Успеваемость': row[2], 'mark': "неудовл."})
        elif 60 < row[2] < 76:
            df_3.append({'Stud_name': row[0], 'Stud_id': row[1], 'Успеваемость': row[2], 'mark': "удовл."})
        elif 75 < row[2] < 91:
            df_4.append({'Stud_name': row[0], 'Stud_id': row[1], 'Успеваемость': row[2], 'mark': "хор."})
        else:
            df_5.append({'Stud_name': row[0], 'Stud_id': row[1], 'Успеваемость': row[2], 'mark': "отл."})

    df_list = [df_2, df_3, df_4, df_5]
    print(df_list)
    response = []
    for list_of_mark in df_list:
        marks = [item["Успеваемость"] for item in list_of_mark]
        if len(marks) > 0:
            response.append({'avg_total_points': sum(marks) / len(marks), 'mark': list_of_mark[0]['mark'],
                             'percent': len(list_of_mark) / len(result_query)})
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response


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
async def attendance_num_for_stud_for_team(id_team: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    sub_query = (
        db.query(
            Lesson.stud_id,
        )
            .filter(and_(Lesson.team_id == id_team))
            .distinct()
            .all()
    )
    stud_id_list = [row[0] for row in sub_query]
    sub_query = (
        db.query(
            Lesson.name,
            (cast(func.count(case([(Lesson.arrival == 'П', 1)], else_=None)), Float)).label("arrival"),
        )
            .filter(and_(Lesson.team_id == id_team, Lesson.stud_id.in_(stud_id_list)))
            .group_by(Lesson.name)
            .all()
    )
    df_list = []
    fix_sort = (
        db.query(
            Lesson.name
        )
            .filter(and_(Lesson.team_id == id_team, Lesson.stud_id == stud_id_list[0]))
            .all()
    )

    for row in sub_query:
        df_list.append({'name': row[0], 'arrival': row[1]})
    df_true = []
    for fixed_row in fix_sort:
        for i in range(len(df_list)):
            if fixed_row[0] in df_list[i]['name']:
                df_true.append(df_list[i])
                break

    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_true


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
async def attendance_num_for_stud_for_team_stat_table(id_team: int, name_of_lesson: str, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    find_missing_studs = (
        db.query(
            Lesson.name.label("lesson_name"),
            Stud.name,
            Stud.id,
            Lesson.id.label("Lesson_id"),
        )
            .filter(Lesson.team_id == id_team, Lesson.name == name_of_lesson, Lesson.arrival != 'П')
            .join(Stud, Stud.id == Lesson.stud_id)
            .group_by(Stud.name, Stud.id, Lesson.name, Lesson.id)
            .all()
    )
    stud_id_list = [item[2] for item in find_missing_studs]
    result_query = (
        db.query(
            Stud.name.label('stud_name'),
            Stud.id,
            Lesson.name,
            Lesson.test,
            Lesson.mark_for_work,
            Lesson.arrival,
            Lesson.date_of_add,
        )
            .filter(and_(Lesson.team_id == id_team, Lesson.stud_id.in_(stud_id_list)))
            .join(Stud, Stud.id == Lesson.stud_id)
            .all()
    )
    dict_stud = {}
    for row in result_query:
        if row[1] not in dict_stud:
            dict_stud[row[1]] = []
        if not any(d['name'] == name_of_lesson for d in dict_stud[row[1]]):
            dict_stud[row[1]].append(
                {'stud_name': row[0], 'id': row[1], 'name': row[2], 'test': row[3], 'mark_for_work': row[4],
                 'arrival': row[5], 'date_of_add': row[6]})
    response_list = []
    for key in dict_stud.keys():
        total_points_temp = (sum(d['test'] for d in dict_stud[key]) + sum(
            d['mark_for_work'] for d in dict_stud[key])) / len(dict_stud[key])
        response_list.append({
            'stud_name': dict_stud[key][0]['stud_name'],
            'id': dict_stud[key][0]['id'],
            'Успеваемость': total_points_temp if total_points_temp >= 0 else 0,
            'Посещаемость': sum(1 for d in dict_stud[key] if d['arrival'] == 'П') / len(dict_stud[key]),
        })
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list


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
async def cum_sum_points_for_stud_for_team(id_team: int, id_stud: int, db=Depends(connect_db_data)):
    await asyncio.sleep(0)
    start_time = time.time()

    result_query = (
        db.query(
            Lesson.name,
            Lesson.test,
            Lesson.mark_for_work,
            Lesson.date_of_add,
        )
            .filter(and_(Lesson.team_id == id_team, Lesson.stud_id == id_stud))
            .all()
    )
    df_list = []
    counter = 1
    for row in result_query:
        df_list.append(
            {'name': row[0], 'test': row[1], 'mark_for_work': row[2], 'date_of_add': row[3], 'counter': counter})
        counter += 1
    df = pd.DataFrame(df_list)
    print(df.head())
    cum_sum = []
    cum_sum.append(0.0)
    response_list = []
    for index, row in df.iterrows():
        cum_sum.append(float(cum_sum[-1]) + float(row['mark_for_work']) + float(row['test']))
        temp = True if row['test'] > 0.0 else False
        response_list.append(
            {'name': row['name'], 'cum_sum': cum_sum[-1] if cum_sum[-1] >= 0 else 0, 'counter': row['counter'],
             'isTest': temp})
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list


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
async def attendance_dynamical_for_stud_for_team(id_team: int, id_stud: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    result_query = (
        db.query(
            Lesson.name,
            Lesson.arrival,
        )
            .filter(and_(Lesson.team_id == id_team, Lesson.stud_id == id_stud))
            .all()
    )
    df_list = []
    for row in result_query:
        df_list.append({'name': row[0], 'arrival': row[1]})
    df = pd.DataFrame(df_list)
    # print(df.head())
    dynamical_arrival = []
    response_list = []
    counter_all = 0
    counter_arrived = 0
    for index, row in df.iterrows():
        if row['arrival'] == "П":
            counter_arrived += 1
        counter_all += 1
        dynamical_arrival.append(float(counter_arrived / counter_all))
        response_list.append({'name': row['name'], 'dynamical_arrival': dynamical_arrival[-1] * 100})

    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list


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
async def attendance_static_for_stud_for_team(id_team: int, id_stud: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    result_query = (
        db.query(
            Lesson.name,
            Lesson.arrival,
        )
            .filter(and_(Lesson.team_id == id_team, Lesson.stud_id == id_stud))
            .all()
    )
    df_list = []
    for row in result_query:
        df_list.append({'name': row[0], 'arrival': row[1]})
    df = pd.DataFrame(df_list)
    # print(df.head())
    static_arrival = []
    response_list = []
    counter_all = len(df_list)
    counter_arrived = 0
    for index, row in df.iterrows():
        if row['arrival'] == "П":
            counter_arrived += 1
        static_arrival.append(float(counter_arrived / counter_all))
        response_list.append({'name': row['name'], 'static_arrival': static_arrival[-1] * 100})

    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list


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
async def attendance_static_stud_for_teams(id_team1: int, id_team2: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    sub_query = (
        db.query(
            Stud.name,
            Stud.id,

            Team.name.label("team_name"),
            (cast(func.count(case([(Lesson.arrival == 'П', 1)], else_=None)), Float) / func.count(
                Lesson.arrival)).label("arrival"),
            Team.id.label("team_id"),
        )
            .filter(or_(Lesson.team_id == id_team1, Lesson.team_id == id_team2)).join(Stud,
                                                                                      Stud.id == Lesson.stud_id).join(
            Team, Team.id == Lesson.team_id)
            .group_by(Stud.name, Stud.id, Team.name, Team.id)
            .all()
    )
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    counter = 0
    for row in sub_query:
        if row[2] not in dict_team:
            dict_team[row[2]] = counter
            counter += 1
        if dict_team[row[2]] == 0:
            team_a.append({'name': row[0], 'id': row[1], 'team_name': row[2], 'arrival': row[3], 'team_id': row[4]})
        elif dict_team[row[2]] == 1:
            team_b.append({'name': row[0], 'id': row[1], 'team_name': row[2], 'arrival': row[3], 'team_id': row[4]})
    team_a.sort(key=lambda x: x['arrival'], reverse=True)
    team_b.sort(key=lambda x: x['arrival'], reverse=True)
    # print(len(team_a))
    # print(len(team_b))

    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    db.close()
    # print(len(df_list))
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
async def total_points_stud_for_teams(id_team1: int, id_team2: int, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()

    sub_query = (
        db.query(
            Stud.name,
            Stud.id,
            Team.name.label("team_name"),
            (func.sum(Lesson.mark_for_work) + func.sum(Lesson.test)).label("total_points"),
            Team.id.label("team_id"),
        )
            .filter(or_(Lesson.team_id == id_team1, Lesson.team_id == id_team2)).join(Stud,
                                                                                      Stud.id == Lesson.stud_id).join(
            Team, Team.id == Lesson.team_id)
            .group_by(Stud.name, Stud.id, Team.name, Team.id)
            .all()
    )
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    counter = 0
    for row in sub_query:
        if row[2] not in dict_team:
            dict_team[row[2]] = counter
            counter += 1
        if dict_team[row[2]] == 0:
            team_a.append(
                {'name': row[0], 'id': row[1], 'team_name': row[2], 'total_points': row[3], 'team_id': row[4]})
        elif dict_team[row[2]] == 1:
            team_b.append(
                {'name': row[0], 'id': row[1], 'team_name': row[2], 'total_points': row[3], 'team_id': row[4]})
    team_a.sort(key=lambda x: x['total_points'], reverse=True)
    team_b.sort(key=lambda x: x['total_points'], reverse=True)
    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    db.close()
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
async def attendance_static_stud_for_all_teams(token: str, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    teams = await get_teams_for_user_private(token, db)
    teams_true = [team[1] for team in teams]
    sub_query = (
        db.query(
            Team.name.label("team_name"),
            (cast(func.count(case([(Lesson.arrival == 'П', 1)], else_=None)), Float) / func.count(
                Lesson.arrival) * 100).label("arrival"),
            Team.id.label("team_id"),
            Teacher.id.label("teacher_id"),
            Teacher.name.label("teacher_name")
        ).filter(Team.name.in_(teams_true))
            .join(Stud, Stud.id == Lesson.stud_id)
            .join(Team, Team.id == Lesson.team_id)
            .join(Teacher, Teacher.id == Lesson.teacher_id)
            .group_by(Team.name, Team.id, Teacher.id, Teacher.name)
            .all()
    )
    df_list = []
    for row in sub_query:
        df_list.append(
            {'team_name': row[0], 'arrival': row[1], 'team_id': row[2], 'teacher_id': row[3], 'teacher_name': row[4]})
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


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
async def total_points_studs_for_all_teams(token: str, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    teams = await get_teams_for_user_private(token, db)
    teams_true = [team[1] for team in teams]
    sub_query = (
        db.query(
            Team.name.label("team_name"),
            func.count(distinct(Stud.id)).label("studs_in_team"),
            ((func.sum(Lesson.mark_for_work) + func.sum(Lesson.test))).label("total_points_sum"),
            Team.id.label("team_id"),
            Teacher.id.label("teacher_id"),
            Teacher.name.label("teacher_name"),
        )
            .filter(Team.name.in_(teams_true))
            .join(Stud, Stud.id == Lesson.stud_id)
            .join(Team, Team.id == Lesson.team_id)
            .join(Teacher, Teacher.id == Lesson.teacher_id)

            .group_by(Team.name, Team.id, Teacher.id, Teacher.name)
            .all()
    )
    df_list = []
    for row in sub_query:
        # print(row[2])
        # print(row[1])
        df_list.append(
            {'team_name': row[0], 'avg_total_points': row[2] / row[1], 'team_id': row[3], 'teacher_id': row[4],
             'teacher_name': row[5]})
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


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
                                             db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = [team[1] for team in teams]
    sub_query = (
        db.query(
            # Team.name.label("team_name"),
            (cast(func.count(case([(Lesson.arrival == 'П', 1)], else_=None)), Float) / func.count(
                Lesson.arrival) * 100).label("arrival"),
            Stud.speciality,
            Stud.id,
        ).filter(Team.name.in_(teams_true), or_(Stud.speciality == speciality1, Stud.speciality == speciality2))
            .join(Stud, Stud.id == Lesson.stud_id)
            .join(Team, Team.id == Lesson.team_id)
            .join(Teacher, Teacher.id == Lesson.teacher_id)
            .group_by(Stud.speciality, Stud.id)
            .all()
    )
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    counter = 0
    for row in sub_query:
        if row[1] not in dict_team:
            dict_team[row[1]] = counter
            counter += 1
        if dict_team[row[1]] == 0:
            team_a.append({'arrival': row[0], 'speciality': row[1], 'id': row[2]})
        elif dict_team[row[1]] == 1:
            team_b.append({'arrival': row[0], 'speciality': row[1], 'id': row[2]})
    team_a.sort(key=lambda x: x['arrival'], reverse=True)
    team_b.sort(key=lambda x: x['arrival'], reverse=True)
    # print(len(team_a))
    # print(len(team_b))

    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    db.close()
    # print(len(df_list))
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
                                        db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = [team[1] for team in teams]
    sub_query = (
        db.query(
            # Team.name.label("team_name"),
            (func.sum(Lesson.mark_for_work) + func.sum(Lesson.test)).label("total_points"),
            Stud.speciality,
            Stud.id,
        ).filter(Team.name.in_(teams_true), or_(Stud.speciality == speciality1, Stud.speciality == speciality2))
            .join(Stud, Stud.id == Lesson.stud_id)
            .join(Team, Team.id == Lesson.team_id)
            .join(Teacher, Teacher.id == Lesson.teacher_id)
            .group_by(Stud.speciality, Stud.id)
            .all()
    )
    df_list = []
    team_a = []
    team_b = []
    dict_team = {}
    counter = 0
    for row in sub_query:
        if row[1] not in dict_team:
            dict_team[row[1]] = counter
            counter += 1
        if dict_team[row[1]] == 0:
            team_a.append({'total_points': row[0], 'speciality': row[1], 'id': row[2]})
        elif dict_team[row[1]] == 1:
            team_b.append({'total_points': row[0], 'speciality': row[1], 'id': row[2]})
    team_a.sort(key=lambda x: x['total_points'], reverse=True)
    team_b.sort(key=lambda x: x['total_points'], reverse=True)
    # print(len(team_a))
    # print(len(team_b))

    for i in range(max(len(team_a), len(team_b))):
        if i < len(team_a):
            df_list.append(team_a[i])
        if i < len(team_b):
            df_list.append(team_b[i])
    db.close()
    # print(len(df_list))
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
async def attendance_static_stud_for_all_specialities(token: str, lect: bool, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = [team[1] for team in teams]
    sub_query = (
        db.query(
            # Team.name.label("team_name"),
            (cast(func.count(case([(Lesson.arrival == 'П', 1)], else_=None)), Float) / func.count(
                Lesson.arrival) * 100).label("arrival"),
            Stud.speciality,
            func.count(distinct(Stud.id)).label("studs_in_speciality"),
        ).filter(Team.name.in_(teams_true))
            .join(Stud, Stud.id == Lesson.stud_id)
            .join(Team, Team.id == Lesson.team_id)
            .join(Teacher, Teacher.id == Lesson.teacher_id)
            .group_by(Stud.speciality)
            .all()
    )
    df_list = []
    for row in sub_query:
        df_list.append(
            {'arrival': row[0], 'Stud_speciality': row[1], 'studs_in_speciality': row[2]})
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


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
async def total_points_studs_for_all_specialities(token: str, lect: bool, db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    if lect:
        teams = await get_teams_for_user_private(token, db)
    else:
        teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = [team[1] for team in teams]
    sub_query = (
        db.query(
            Stud.speciality,
            func.count(distinct(Stud.id)).label("studs_in_speciality"),
            (func.sum(Lesson.mark_for_work) + func.sum(Lesson.test)).label("total_points_sum"),
        )
            .filter(Team.name.in_(teams_true))
            .join(Stud, Stud.id == Lesson.stud_id)
            .join(Team, Team.id == Lesson.team_id)
            .join(Teacher, Teacher.id == Lesson.teacher_id)
            .group_by(Stud.speciality)
            .all()
    )
    df_list = []
    for row in sub_query:
        # print(row[2])
        # print(row[1])
        df_list.append(
            {'Stud_speciality': row[0], 'avg_total_points': row[2] / row[1], 'studs_in_speciality': row[1]})
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return df_list


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
async def kr_analyse_simple(token: str, type: int, kr: str,
                            db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    teams = await get_teams_for_user_private_without_lect(token, db)
    teams_true = [team[1] for team in teams]
    # teachers = await get_all_teachers(token,db)
    # teachers_true = [team[1] for team in teachers]
    # print(teams_true)
    match type:
        case 0:
            print("Группировка по командам")
            sub_query = (
                db.query(
                    # Team.name.label("team_name"),
                    Lesson.test,
                    Team.name,
                ).filter(Team.name.in_(teams_true), Lesson.name == kr
                         # , Teacher.name.in_(teachers_true)
                         )
                    .join(Stud, Stud.id == Lesson.stud_id)
                    .join(Team, Team.id == Lesson.team_id)
                    .join(Teacher, Teacher.id == Lesson.teacher_id)
                    .all()
            )
        case 1:
            print("Группировка по направлениям")
            sub_query = (
                db.query(
                    # Team.name.label("team_name"),
                    Lesson.test,
                    Stud.speciality,
                ).filter(Team.name.in_(teams_true), Lesson.name == kr
                         # , Teacher.name.in_(teachers_true)
                         )
                    .join(Stud, Stud.id == Lesson.stud_id)
                    .join(Team, Team.id == Lesson.team_id)
                    .join(Teacher, Teacher.id == Lesson.teacher_id)
                    .all()
            )
        case 2:
            print("Группировка по преподавателям")
            sub_query = (
                db.query(
                    # Team.name.label("team_name"),
                    Lesson.test,
                    Teacher.name,
                ).filter(Team.name.in_(teams_true), Lesson.name == kr
                         # , Teacher.name.in_(teachers_true)
                         )
                    .join(Stud, Stud.id == Lesson.stud_id)
                    .join(Team, Team.id == Lesson.team_id)
                    .join(Teacher, Teacher.id == Lesson.teacher_id)
                    .all()
            )
        case _:
            db.close()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Неправильно выбран тип 0 - Группировка по командам, 1 - " +
                                       "Группировка по направлениям, 2 - Группировка по преподавателям")
    print(len(sub_query))
    dict_of_teams = {}
    for row in sub_query:
        if row[1] not in dict_of_teams:
            dict_of_teams[row[1]] = []
        dict_of_teams[row[1]].append(row[0])
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return dict_of_teams


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
                                  db=Depends(connect_db_data)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    if teacher is None:
        teachers = await get_all_teachers(token, db)
        teachers = [item[1] for item in teachers]
    else:
        teachers = [teacher]
    if speciality is None:
        specialities = await get_all_specialities(token, db)
        specialities = [item[0] for item in specialities]
    else:
        specialities = [speciality]
    if team is None:
        teams = await get_teams_for_user_private_without_lect(token, db)
        teams = [item[1] for item in teams]
    else:
        teams = [team]
    sub_query = (
        db.query(
            # Team.name.label("team_name"),
            Lesson.test,
            Team.name.label("Название команды"),
            Teacher.name.label("ФИО преподавателя"),
            Stud.speciality.label("Название направления обучения"),
        ).filter(Team.name.in_(teams), Lesson.name == kr, Teacher.name.in_(teachers), Stud.speciality.in_(specialities))
            .join(Stud, Stud.id == Lesson.stud_id)
            .join(Team, Team.id == Lesson.team_id)
            .join(Teacher, Teacher.id == Lesson.teacher_id)
            .all()
    )
    print(len(sub_query))
    dict_of_teams = {}
    match type_select:
        case 0:
            for row in sub_query:
                key = row[1]
                if key not in dict_of_teams:
                    dict_of_teams[key] = []
                dict_of_teams[key].append(row[0])
        case 1:
            for row in sub_query:
                key = row[2]
                if key not in dict_of_teams:
                    dict_of_teams[key] = []
                dict_of_teams[key].append(row[0])
        case 2:
            for row in sub_query:
                key = row[3]
                if key not in dict_of_teams:
                    dict_of_teams[key] = []
                dict_of_teams[key].append(row[0])
        case 3:
            for row in sub_query:
                key = row[1] + ' ' + row[2]
                if key not in dict_of_teams:
                    dict_of_teams[key] = []
                dict_of_teams[key].append(row[0])
        case 4:
            for row in sub_query:
                key = row[1] + ' ' + row[3]
                if key not in dict_of_teams:
                    dict_of_teams[key] = []
                dict_of_teams[key].append(row[0])
        case 5:
            for row in sub_query:
                key = row[2] + ' ' + row[3]
                if key not in dict_of_teams:
                    dict_of_teams[key] = []
                dict_of_teams[key].append(row[0])
        case 6:
            for row in sub_query:
                key = row[1] + ' ' + row[2] + ' ' + row[3]
                if key not in dict_of_teams:
                    dict_of_teams[key] = []
                dict_of_teams[key].append(row[0])
        case _:
            db.close()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Неправильно выбран тип(всего их 0,1,2,3,4,5,6)")

    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return dict_of_teams
# endregion

# @router.get('/api/tolko_chto_dobavil', name='Plot:plot', status_code=status.HTTP_200_OK,
#             tags=["kr page"], description=
#             """
#                     Получает token: str, kr: str, type:int, teacher: Optional[str] = None, speciality: Optional[str] = None,
#                                   team: Optional[str] = None,
#                     Returns:
#                         Словарь с ключами(преподаватели/аправления/команды) и любые их сочетания(проверь чтоб понять)
#                     \n
#                     {
#                       "Трефилин Иван Андреевич": [
#                         12,
#                         0,
#                         14.43,
#                         3,
#                         6.83,
#                         12.3,
#                         2,
#             """)
# async def tolko_chto_dobavil(token: str,
#                                   db=Depends(connect_db_data)):
#     # Create your plot using Plotly
#     await asyncio.sleep(0)
#     print(token)
#     return token