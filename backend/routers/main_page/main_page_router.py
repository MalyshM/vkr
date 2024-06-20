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
                                  массив словарей (stud_name, stud_id, Посещаемость)
                              \n
                              [
                                {
                                  "stud_name": "297fa3e7b1df9f4e503ff4b76a9806be595bc79c38687b7c2d0d6301ec8eb04e",
                                  "stud_id": 86,
                                  "Посещаемость": 0.8636363636363636
                                },
                                {
                                  "stud_name": "391c01a02b6fd2ffd532b8ee8b3b8f6c91d3082f220680904b042469b3beaea1",
                                  "stud_id": 231,
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
                ROUND(count(id) filter (where l.arrival ='П') over (partition by stud_id) * 100 / count(id) over (partition by stud_id)::DECIMAL, 2) as "Посещаемость"
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
                                  массив словарей ("Успеваемость_средняя", "Посещаемость_средняя", "stud_name", "stud_id", "Посещаемость", "Успеваемость")\n
                              [
                                {
                                    "Успеваемость_средняя": 76.6,
                                    "Посещаемость_средняя": 86.36,
                                    "stud_name": "02045b53c0b6bff0153cbc64ff850efcdd448e6886740e97f5ad868083afb720",
                                    "stud_id": 959,
                                    "Посещаемость": 86.36,
                                    "Успеваемость": 62.51
                                },
                                {
                                    "Успеваемость_средняя": 76.6,
                                    "Посещаемость_средняя": 86.36,
                                    "stud_name": "0d51af0f0062a519266207f4b540d5136a979172b8c47a3bd9e7e63d718cef12",
                                    "stud_id": 197,
                                    "Посещаемость": 95.45,
                                    "Успеваемость": 77
                                },
                                ...
                                {
                                    "Успеваемость_средняя": 76.6,
                                    "Посещаемость_средняя": 86.36,
                                    "stud_name": "f7cd34b508d881e78766d70c591dc1eb34f7cae3887d927c0d2779d0046edd8c",
                                    "stud_id": 814,
                                    "Посещаемость": 54.55,
                                    "Успеваемость": 63
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
            SELECT *
            FROM (
                SELECT
                    ROUND(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sub."Успеваемость")::DECIMAL, 2) AS "Успеваемость_средняя",
                    ROUND(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sub."Посещаемость")::DECIMAL, 2) AS "Посещаемость_средняя"
                FROM (
                    SELECT DISTINCT
                        (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS "stud_name",
                        (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS "stud_id",
                        ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY stud_id) * 100 / COUNT(id) OVER (PARTITION BY stud_id)::DECIMAL, 2) AS "Посещаемость",
                        ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id) + SUM(l.test) OVER (PARTITION BY stud_id))::DECIMAL, 2) AS "Успеваемость"
                    FROM
                        lesson l
                    WHERE
                        l.team_id = {id_team}
                ) AS sub
            ) AS sub,
            (
                SELECT DISTINCT
                    (SELECT s.name FROM stud s WHERE s.id = l.stud_id) AS "stud_name",
                    (SELECT s.id FROM stud s WHERE s.id = l.stud_id) AS "stud_id",
                    ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY stud_id) * 100 / COUNT(id) OVER (PARTITION BY stud_id)::DECIMAL, 2) AS "Посещаемость",
                    ROUND((SUM(l.mark_for_work) OVER (PARTITION BY stud_id) + SUM(l.test) OVER (PARTITION BY stud_id))::DECIMAL, 2) AS "Успеваемость"
                FROM
                    lesson l
                WHERE
                    l.team_id = {id_team}
            ) AS sub1;
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
                                  массив словарей ("stud_name", "stud_id", "Успеваемость")\n
                              [
                                {
                                  "stud_name": "297fa3e7b1df9f4e503ff4b76a9806be595bc79c38687b7c2d0d6301ec8eb04e",
                                  "stud_id": 86,
                                  "Успеваемость": 77.5
                                },
                                {
                                  "stud_name": "391c01a02b6fd2ffd532b8ee8b3b8f6c91d3082f220680904b042469b3beaea1",
                                  "stud_id": 231,
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
                                  массив словарей ("mark","percent", "avg_total_points")
                              \n
                            [
                              {
                                "mark": "неудовл.",
                                "percent": 0.13,
                                "avg_total_points": 7
                              },
                              {
                                "mark": "отл.",
                                "percent": 0.13,
                                "avg_total_points": 91
                              },
                              {
                                "mark": "удовл.",
                                "percent": 0.2,
                                "avg_total_points": 63
                              },
                              {
                                "mark": "хор.",
                                "percent": 0.53,
                                "avg_total_points": 77
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
                ROUND(PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY sub."Успеваемость")::DECIMAL, 2) AS avg_total_points
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
                                  массив словарей ("name", "id", "Посещаемость")\n
                              [
                                {
                                    "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных00",
                                    "id": 7,
                                    "Посещаемость": 23
                                  },
                                  {
                                    "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных10",
                                    "id": 8,
                                    "Посещаемость": 28
                                  },
                                  {
                                    "name": "Основные принципы организации Языка Python. Базовые элементы программирования и типы данных20",
                                    "id": 9,
                                    "Посещаемость": 28
                                  },
                                  {
                                    "name": "Управляющие конструкции00",
                                    "id": 10,
                                    "Посещаемость": 24
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
                                  массив словарей "stud_name", "id", "Посещаемость", "Успеваемость"\n
                                [
                                  {
                                    "stud_name": "9c62c954dd8e44297cfc1e537eaf1c8bb82ae21fa3b6b0b56530759943771e51",
                                    "id": 30,
                                    "Посещаемость": 1,
                                    "Успеваемость": 2
                                  },
                                  {
                                    "stud_name": "275ae623ccbfa5b1749c13398b8b580d9aed00833a6572e96aeb3afbb733ea23",
                                    "id": 144,
                                    "Посещаемость": 3,
                                    "Успеваемость": 8
                                  },
                                  {
                                    "stud_name": "5c7bc1785529427017234aa2cfc9da6ce6f09f59fec4f486b82b44b4067b1bb3",
                                    "id": 165,
                                    "Посещаемость": 2,
                                    "Успеваемость": 8
                                  },
                                  {
                                    "stud_name": "5b4ee33933c8eae279e6142a374b77350dd5dac1494b523b5f10a6f7b53ef4fe",
                                    "id": 442,
                                    "Посещаемость": 2,
                                    "Успеваемость": 2
                                  },
                                  {
                                    "stud_name": "e09244f5531362498e842225a652e717543be0a198894356798572eae7b78fa3",
                                    "id": 688,
                                    "Посещаемость": 2,
                                    "Успеваемость": 8
                                  },
                                  {
                                    "stud_name": "4c9fe52d7d80a8fc7173f862cc7d6bfd7107c4e9ba5ebec2470628d085f25729",
                                    "id": 880,
                                    "Посещаемость": 0,
                                    "Успеваемость": 0
                                  }
                                ]
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
                ROUND(COUNT(id) FILTER (WHERE l.arrival = 'П') OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) * 100 / COUNT(id) OVER (PARTITION BY l.stud_id ORDER BY l.id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)::DECIMAL, 2) AS Посещаемость,
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
