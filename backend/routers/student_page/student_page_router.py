import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger import LOGGER
from models import connect_db_data
from redis import process_href, save_resp_and_return_it

student_page_router = APIRouter(tags=["Student page"])


@student_page_router.get('/api/cum_sum_points_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
                         description=
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
    href = f"cum_sum_points_for_stud_for_team-{id_team}-{id_stud}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        result_query = await db.execute(f"""
                SELECT
                    l.name,
                    ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) + SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW))::DECIMAL, 2) AS cum_sum,
                    row_number() over (PARTITION BY stud_id) as counter,
                    CASE
                        WHEN l.test  >= 0 THEN true
                        ELSE false
                    END AS test
                  FROM
                    lesson l
                  WHERE
                    l.team_id = {id_team} and l.stud_id = {id_stud}
                        """)
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@student_page_router.get('/api/attendance_dynamical_for_stud_for_team', name='Plot:plot',
                         status_code=status.HTTP_200_OK,
                         description=
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
    href = f"attendance_dynamical_for_stud_for_team-{id_team}-{id_stud}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        result_query = await db.execute(f"""
                SELECT
                    l.name,
                    ROUND((COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 100) / COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL, 2) AS dynamical_arrival
                  FROM
                    lesson l
                  WHERE
                    l.team_id = {id_team} and l.stud_id = {id_stud}
                        """)
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@student_page_router.get('/api/attendance_static_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
                         description=
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
    href = f"attendance_static_for_stud_for_team-{id_team}-{id_stud}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        result_query = await db.execute(f"""
                SELECT
                    l.name,
                    ROUND((COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 100) / COUNT(id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS static_arrival
                  FROM
                    lesson l
                  WHERE
                    l.team_id = {id_team} and l.stud_id = {id_stud}
                        """)
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@student_page_router.get('/api/all_in_one_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
                         description=
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
    href = f"all_in_one_for_stud_for_team-{id_team}-{id_stud}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        result_query = await db.execute(f"""
            SELECT
                l.name,
                ROUND((COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 100) / COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL, 2) AS dynamical_arrival,
                ROUND((COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 100) / COUNT(id) OVER (PARTITION BY l.stud_id)::DECIMAL, 2) AS static_arrival,
                ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) + SUM(l.test) OVER (PARTITION BY stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW))::DECIMAL, 2) AS cum_sum,
                row_number() over (PARTITION BY stud_id) as counter,
                CASE
                    WHEN l.test  >= 0 THEN true
                    ELSE false
                END AS test
              FROM
                lesson l
              WHERE
                l.team_id = {id_team} and l.stud_id = {id_stud}
                    """)
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
