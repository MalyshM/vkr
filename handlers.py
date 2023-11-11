import ast
import asyncio
import datetime
import json
import time
from fastapi import APIRouter, Query, Depends
from sqlalchemy.dialects.postgresql import JSONB
from starlette import status
from models import connect_db
from sqlalchemy import func

router = APIRouter()


@router.get('/get_all_mark_of_subject_of_control', name='Plot:plot', status_code=status.HTTP_200_OK,
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
async def get_all_mark_of_subject_of_control(id: int, db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    result_query = db.query(func.avg(TableForAll.result_points), TableForAll.name_of_student).group_by(
        TableForAll.name_of_student).all()
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    # print(result_query)
    response_list = []
    for row in result_query:
        response_list.append({
            "Итоговые баллы": row[0],
            "ФИО студента": row[1]})
    return response_list


@router.get('/get_mark_of_subject_of_control_of_student', name='Plot:plot', status_code=status.HTTP_200_OK,
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
async def get_mark_of_subject_of_control_of_student(name_of_student: str, db=Depends(connect_db)):
    # Create your plot using Plotly
    await asyncio.sleep(0)
    start_time = time.time()
    result_query = db.query(TableForAll.mark_of_subject_of_control, TableForAll.subject_of_control,
                            TableForAll.name_of_student).filter(TableForAll.name_of_student == name_of_student).all()
    db.close()
    print("--- %s seconds ---" % (time.time() - start_time), end=" finish\n")
    # print(result_query)
    response_list = []
    for row in result_query:
        try:
            grade = float(row[0])
        except ValueError:
            grade = row[0]
        response_list.append({
                "Оценка за предмет контроля": grade,
                "Предмет контроля": row[1],
                "ФИО студента": row[2]})
    return response_list
