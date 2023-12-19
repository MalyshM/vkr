import ast
import asyncio
from datetime import datetime, timedelta
import json
import time
from typing import Annotated

import pandas as pd
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Query, Depends
from sqlalchemy.dialects.postgresql import JSONB
from starlette import status
from sqlalchemy.sql.expression import and_, case, cast, or_
from starlette.exceptions import HTTPException

from schemas import UserRegistration, TokenData, UserLogin
from util import Hasher
from models import connect_db_data, connect_db_users, Lesson, Team, User, Stud, Teacher
from sqlalchemy import func, Integer, Float
import jwt

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
             tags=["Registration"])
async def registration_standard(user: UserRegistration, db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    checkuser = db.query(User).filter(and_(User.username == user.username, User.email == user.email)).first()
    if checkuser is not None:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Вам не взломать пентагон")

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
             tags=["User"])
async def get_current_user_dev(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
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


@router.get('/api/get_all_users', name='User:get_all_users', status_code=status.HTTP_200_OK, tags=["User"])
async def get_all_users(db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    all_users = db.query(User).all()
    return all_users


@router.get('/api/delete_all_users', name='User:delete_all_users', status_code=status.HTTP_200_OK, tags=["User"])
async def delete_all_users(db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    db.query(User).delete()
    db.commit()
    return {"message": "All users deleted successfully"}


@router.post('/api/login_standard', name='Registration:login_standard', status_code=status.HTTP_200_OK,
             tags=["Registration"])
async def login_standard(user: UserLogin, db=Depends(connect_db_users)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    checkuser = db.query(User).filter(and_(User.username == user.username, User.email == user.email)).first()
    print(checkuser)
    if checkuser is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Вам не взломать пентагон")
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
        return "not logged"


@router.get('/api/get_teams_for_user', name='Team:get_teams_for_user', status_code=status.HTTP_200_OK,
            tags=["Team"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
        return "в доступе отказано"


@router.get('/api/attendance_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
    # print(result_query)
    # response_list = []
    # for row in result_query:
    #     response_list.append({
    #         "Итоговые баллы": row[0],
    #         "ФИО студента": row[1]})
    return result_query


@router.get('/api/total_points_attendance_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
            """)
async def total_points_per_stud_for_team(id_team: int, db=Depends(connect_db_data)):
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
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    # print(result_query)
    # response_list = []
    # for row in result_query:
    #     response_list.append({
    #         "Итоговые баллы": row[0],
    #         "ФИО студента": row[1]})
    return result_query


@router.get('/api/total_points_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
    # print(result_query)
    # response_list = []
    # for row in result_query:
    #     response_list.append({
    #         "Итоговые баллы": row[0],
    #         "ФИО студента": row[1]})
    return result_query


@router.get('/api/cum_sum_points_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
            {'name': row['name'], 'cum_sum': cum_sum[-1], 'counter': row['counter'], 'isTest': temp})
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    return response_list


@router.get('/api/attendance_dynamical_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
    print(df.head())
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


@router.get('/api/attendance_num_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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


@router.get('/api/attendance_static_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
    print(df.head())
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


@router.get('/api/attendance_static_stud_for_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
        )
            .filter(or_(Lesson.team_id == id_team1, Lesson.team_id == id_team2)).join(Stud,
                                                                                      Stud.id == Lesson.stud_id).join(
            Team, Team.id == Lesson.team_id)
            .group_by(Stud.name, Stud.id, Team.name)
            .subquery()
    )
    result_query = (
        db.query(
            sub_query.c.team_name,
            func.avg(sub_query.c.arrival).label("arrival_avg"),
        )
            .group_by(sub_query.c.team_name)
            .all()
    )
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    # print(result_query)
    # response_list = []
    # for row in result_query:
    #     response_list.append({
    #         "Итоговые баллы": row[0],
    #         "ФИО студента": row[1]})
    return result_query


@router.get('/api/total_points_stud_for_teams', name='Plot:plot', status_code=status.HTTP_200_OK,
            tags=["Plot"], description=
            """
                    Получает продавца по id

                    Args:
                        from_ (int): С какой записи начать.
                        to    (int): Какой записью закончить.
                        limit (int): Сколько записей брать.
                    Raises:
                        HTTPException: Raises, если хоть одно условие выполняется db.query(Seller).filter(Seller.id == id).all() is None or (
            type(id) != type(0)).

                    Returns:
                        List[Seller]: список продавцов.
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
            (func.sum(Lesson.mark_for_work) + func.sum(Lesson.test)).label("total_points")
        )
            .filter(or_(Lesson.team_id == id_team1, Lesson.team_id == id_team2)).join(Stud,
                                                                                      Stud.id == Lesson.stud_id).join(
            Team, Team.id == Lesson.team_id)
            .group_by(Stud.name, Stud.id, Team.name)
            .subquery()
    )
    result_query = (
        db.query(
            sub_query.c.team_name,
            func.avg(sub_query.c.total_points).label("total_points_avg"),
        )
            .group_by(sub_query.c.team_name)
            .all()
    )
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    # print(result_query)
    # response_list = []
    # for row in result_query:
    #     response_list.append({
    #         "Итоговые баллы": row[0],
    #         "ФИО студента": row[1]})
    return result_query
