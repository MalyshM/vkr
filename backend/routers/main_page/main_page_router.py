import time

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from logger import LOGGER
from models import connect_db_data
from redis import process_href, save_resp_and_return_it

main_page_router = APIRouter(tags=["Main page"])


@main_page_router.get('/api/attendance_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
                      description=
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
    href = f"attendance_per_stud_for_team-{id_team}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
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
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@main_page_router.get('/api/total_points_attendance_per_stud_for_team', name='Plot:plot',
                      status_code=status.HTTP_200_OK,
                      description=
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
    href = f"total_points_attendance_per_stud_for_team-{id_team}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
        result_query = await db.execute(f"""
            select *, avg(sub."Успеваемость") over (partition by "Посещаемость_средняя") as "Успеваемость_средняя"
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
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@main_page_router.get('/api/total_points_per_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
                      description=
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
    href = f"total_points_per_stud_for_team-{id_team}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
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
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@main_page_router.get('/api/total_marks_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
                      description=
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
    href = f"total_marks_for_team-{id_team}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
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
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@main_page_router.get('/api/attendance_num_for_stud_for_team', name='Plot:plot', status_code=status.HTTP_200_OK,
                      description=
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
    href = f"attendance_num_for_stud_for_team-{id_team}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
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
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e


@main_page_router.get('/api/attendance_num_for_stud_for_team_stat_table', name='Plot:plot',
                      status_code=status.HTTP_200_OK,
                      description=
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
    href = f"attendance_num_for_stud_for_team_stat_table-{id_team}-{name_of_lesson}"
    LOGGER.info(f"{href} start")
    res = await process_href(href, start_time)
    if res is not None:
        return res
    try:
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
        result = result_query.fetchall()
        return await save_resp_and_return_it(result, href, start_time)
    except Exception as e:
        LOGGER.error(f"{href} Error {e}")
        raise e
